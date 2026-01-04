import os
from queue import Queue
from threading import Thread
from typing import List, Dict, Callable, Optional
from PyQt6.QtCore import QObject, pyqtSignal, QMutex
import logging

from api_clients import DoubaoClient, BananaClient, image_to_base64

logger = logging.getLogger(__name__)


class ProcessingTask:
    """Represents a single image processing task."""
    
    def __init__(self, image_path: str, output_dir: str, model_type: str, model_params: Dict):
        self.image_path = image_path
        self.output_dir = output_dir
        self.model_type = model_type
        self.model_params = model_params
        self.success = False
        self.error_message = None
        self.output_path = None


class WorkerThread(Thread):
    """Worker thread for processing a single image."""
    
    def __init__(self, task: ProcessingTask, config: Dict[str, str], 
                 progress_callback: Optional[Callable[[str, bool, Optional[str]], None]] = None):
        super().__init__()
        self.task = task
        self.config = config
        self.progress_callback = progress_callback
    
    def run(self):
        """Process the image according to the task specification."""
        try:
            # Convert image to base64
            image_base64 = image_to_base64(self.task.image_path)
            
            # Generate output filename
            base_name = os.path.splitext(os.path.basename(self.task.image_path))[0]
            output_filename = f"{base_name}_processed.png"
            self.task.output_path = os.path.join(self.task.output_dir, output_filename)
            
            # Call appropriate API based on model type
            if self.task.model_type == 'doubao':
                self._process_doubao(image_base64)
            elif self.task.model_type == 'banana':
                self._process_banana(image_base64)
            else:
                raise ValueError(f"Unknown model type: {self.task.model_type}")
            
            # Save processed image
            if self.task.success and self.task.result_bytes:
                with open(self.task.output_path, 'wb') as f:
                    f.write(self.task.result_bytes)
                logger.info(f"Successfully saved processed image: {self.task.output_path}")
            
        except Exception as e:
            self.task.success = False
            self.task.error_message = str(e)
            logger.error(f"Task failed for {self.task.image_path}: {str(e)}")
        
        # Notify completion
        if self.progress_callback:
            self.progress_callback(self.task.image_path, self.task.success, self.task.error_message)
    
    def _process_doubao(self, image_base64: str):
        """Process image using Doubao API."""
        client = DoubaoClient(
            api_url=self.config['doubao_api_url'],
            api_key=self.config['doubao_api_key']
        )
        
        success, error_msg, image_bytes = client.edit_image(
            image_base64=image_base64,
            edit_type=self.task.model_params.get('edit_type', 'retouch'),
            smooth=float(self.task.model_params.get('smooth', 0.8)),
            whiten=float(self.task.model_params.get('whiten', 0.6))
        )
        
        self.task.success = success
        self.task.error_message = error_msg
        self.task.result_bytes = image_bytes
    
    def _process_banana(self, image_base64: str):
        """Process image using Banana API."""
        client = BananaClient(
            api_url=self.config['banana_api_url'],
            api_key=self.config['banana_api_key'],
            model_key=self.config['banana_model_key']
        )
        
        success, error_msg, image_bytes = client.apply_style(
            image_base64=image_base64,
            prompt=self.task.model_params.get('prompt', 'convert to anime style, high detail')
        )
        
        self.task.success = success
        self.task.error_message = error_msg
        self.task.result_bytes = image_bytes


class TaskManager(QObject):
    """Manages task queue and worker threads."""
    
    # Signals
    progress_update = pyqtSignal(int, int)  # (completed, total)
    task_completed = pyqtSignal(str, bool, str)  # (image_path, success, error_message)
    all_completed = pyqtSignal(int, int)  # (success_count, failure_count)
    
    def __init__(self, max_workers: int = 5):
        super().__init__()
        self.max_workers = max_workers
        self.task_queue = Queue()
        self.active_workers = 0
        self.mutex = QMutex()
        self.is_running = False
        
        self.completed_count = 0
        self.success_count = 0
        self.failure_count = 0
        self.total_tasks = 0
    
    def add_tasks(self, tasks: List[ProcessingTask]):
        """Add tasks to the queue."""
        self.total_tasks += len(tasks)
        for task in tasks:
            self.task_queue.put(task)
    
    def start(self, config: Dict[str, str]):
        """Start processing tasks."""
        if self.is_running:
            return
        
        self.is_running = True
        self.completed_count = 0
        self.success_count = 0
        self.failure_count = 0
        
        # Start worker threads
        for _ in range(self.max_workers):
            thread = Thread(target=self._worker_loop, args=(config,), daemon=True)
            thread.start()
    
    def _worker_loop(self, config: Dict[str, str]):
        """Worker thread main loop."""
        while self.is_running:
            try:
                # Get task from queue (with timeout to allow checking is_running)
                task = self.task_queue.get(timeout=0.1)
                
                # Process task
                worker = WorkerThread(task, config, self._on_task_completed)
                worker.run()
                
                # Mark task as done
                self.task_queue.task_done()
                
            except:
                # Queue empty or timeout
                if self.task_queue.empty():
                    self.mutex.lock()
                    if self.active_workers == 0 and self.task_queue.empty():
                        self.is_running = False
                        self.all_completed.emit(self.success_count, self.failure_count)
                    self.mutex.unlock()
    
    def _on_task_completed(self, image_path: str, success: bool, error_message: Optional[str]):
        """Called when a task completes."""
        self.mutex.lock()
        
        self.completed_count += 1
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
        
        self.mutex.unlock()
        
        # Emit signals
        self.progress_update.emit(self.completed_count, self.total_tasks)
        self.task_completed.emit(image_path, success, error_message or '')
        
        # Check if all tasks completed
        if self.completed_count >= self.total_tasks:
            self.is_running = False
            self.all_completed.emit(self.success_count, self.failure_count)
    
    def stop(self):
        """Stop all processing."""
        self.is_running = False
