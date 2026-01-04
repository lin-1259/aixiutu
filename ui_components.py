import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel, QComboBox, QLineEdit,
    QProgressBar, QDialog, QFormLayout, QDialogButtonBox,
    QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage
from typing import Optional, List, Dict

from config_manager import ConfigManager
from worker_threads import ProcessingTask, TaskManager


class ApiConfigDialog(QDialog):
    """Dialog for configuring API settings."""
    
    def __init__(self, config: Dict[str, str], parent=None):
        super().__init__(parent)
        self.config = config.copy()
        self.result_config = None
        self._init_ui()
    
    def _init_ui(self):
        self.setWindowTitle('API 配置')
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Form layout for configuration items
        form_layout = QFormLayout()
        
        # Doubao API Configuration
        self.doubao_url_input = QLineEdit(self.config.get('doubao_api_url', ''))
        self.doubao_key_input = QLineEdit(self.config.get('doubao_api_key', ''))
        self.doubao_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow('豆包 API 地址:', self.doubao_url_input)
        form_layout.addRow('豆包 API Key:', self.doubao_key_input)
        
        # Banana API Configuration
        self.banana_url_input = QLineEdit(self.config.get('banana_api_url', ''))
        self.banana_key_input = QLineEdit(self.config.get('banana_api_key', ''))
        self.banana_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.banana_model_key_input = QLineEdit(self.config.get('banana_model_key', ''))
        
        form_layout.addRow('Banana API 地址:', self.banana_url_input)
        form_layout.addRow('Banana API Key:', self.banana_key_input)
        form_layout.addRow('Banana 模型 Key:', self.banana_model_key_input)
        
        layout.addLayout(form_layout)
        
        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._on_ok)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _on_ok(self):
        """Validate and save configuration."""
        result = {
            'doubao_api_url': self.doubao_url_input.text().strip(),
            'doubao_api_key': self.doubao_key_input.text().strip(),
            'banana_api_url': self.banana_url_input.text().strip(),
            'banana_api_key': self.banana_key_input.text().strip(),
            'banana_model_key': self.banana_model_key_input.text().strip()
        }
        
        # Basic validation
        if not all(result.values()):
            QMessageBox.warning(self, '配置不完整', '所有配置项都必须填写！')
            return
        
        self.result_config = result
        self.accept()


class PreviewPanel(QWidget):
    """Panel for displaying before/after image preview."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_original_path: Optional[str] = None
        self.current_processed_path: Optional[str] = None
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Splitter for vertical layout
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Original image panel
        original_frame = QFrame()
        original_frame.setFrameShape(QFrame.Shape.StyledPanel)
        original_layout = QVBoxLayout(original_frame)
        original_layout.setContentsMargins(5, 5, 5, 5)
        
        original_label = QLabel('原图')
        original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        original_label.setStyleSheet('font-weight: bold; padding: 5px;')
        
        self.original_image_label = QLabel()
        self.original_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_image_label.setStyleSheet('background-color: #f0f0f0; border: 1px solid #ccc;')
        self.original_image_label.setMinimumSize(200, 200)
        self.original_image_label.setText('请选择图片预览')
        
        original_layout.addWidget(original_label)
        original_layout.addWidget(self.original_image_label, 1)
        
        # Processed image panel
        processed_frame = QFrame()
        processed_frame.setFrameShape(QFrame.Shape.StyledPanel)
        processed_layout = QVBoxLayout(processed_frame)
        processed_layout.setContentsMargins(5, 5, 5, 5)
        
        processed_label = QLabel('处理后效果图')
        processed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        processed_label.setStyleSheet('font-weight: bold; padding: 5px;')
        
        self.processed_image_label = QLabel()
        self.processed_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.processed_image_label.setStyleSheet('background-color: #f0f0f0; border: 1px solid #ccc;')
        self.processed_image_label.setMinimumSize(200, 200)
        self.processed_image_label.setText('等待处理...')
        
        processed_layout.addWidget(processed_label)
        processed_layout.addWidget(self.processed_image_label, 1)
        
        # Add frames to splitter
        splitter.addWidget(original_frame)
        splitter.addWidget(processed_frame)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)
    
    def set_original_image(self, image_path: str):
        """Display original image."""
        self.current_original_path = image_path
        self._display_image(self.original_image_label, image_path)
    
    def set_processed_image(self, image_path: str):
        """Display processed image."""
        self.current_processed_path = image_path
        self._display_image(self.processed_image_label, image_path)
    
    def _display_image(self, label: QLabel, image_path: str):
        """Load and display image on label."""
        try:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                label.setText('无法加载图片')
                return
            
            # Scale image to fit label while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            label.setText(f'加载失败: {str(e)}')
    
    def clear_processed(self):
        """Clear processed image display."""
        self.current_processed_path = None
        self.processed_image_label.clear()
        self.processed_image_label.setText('等待处理...')
    
    def resizeEvent(self, event):
        """Handle resize event to update image display."""
        super().resizeEvent(event)
        
        if self.current_original_path:
            self._display_image(self.original_image_label, self.current_original_path)
        
        if self.current_processed_path:
            self._display_image(self.processed_image_label, self.current_processed_path)


class ConfigPanel(QWidget):
    """Left panel for configuration."""
    
    # Signals
    import_clicked = pyqtSignal()
    api_config_clicked = pyqtSignal()
    output_dir_clicked = pyqtSignal()
    start_processing = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_paths: List[str] = []
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # API Configuration Button
        self.api_config_btn = QPushButton('API 配置')
        self.api_config_btn.clicked.connect(self.api_config_clicked.emit)
        layout.addWidget(self.api_config_btn)
        
        # Separator
        self._add_separator(layout)
        
        # Image Import
        import_label = QLabel('图片导入')
        import_label.setStyleSheet('font-weight: bold;')
        layout.addWidget(import_label)
        
        self.import_btn = QPushButton('导入图片')
        self.import_btn.clicked.connect(self.import_clicked.emit)
        layout.addWidget(self.import_btn)
        
        self.image_list = QListWidget()
        self.image_list.currentRowChanged.connect(self._on_image_selected)
        layout.addWidget(self.image_list)
        
        # Separator
        self._add_separator(layout)
        
        # Model Selection
        model_label = QLabel('模型选择')
        model_label.setStyleSheet('font-weight: bold;')
        layout.addWidget(model_label)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems(['豆包修图模型', 'Banana 风格模型'])
        self.model_combo.currentIndexChanged.connect(self._on_model_changed)
        layout.addWidget(self.model_combo)
        
        # Doubao parameters panel
        self.doubao_panel = QWidget()
        doubao_layout = QVBoxLayout(self.doubao_panel)
        
        doubao_layout.addWidget(QLabel('修图类型:'))
        self.doubao_type_combo = QComboBox()
        self.doubao_type_combo.addItems(['retouch', 'enhance'])
        self.doubao_type_combo.setItemText(0, '人像精修 (retouch)')
        self.doubao_type_combo.setItemText(1, '画质增强 (enhance)')
        doubao_layout.addWidget(self.doubao_type_combo)
        
        doubao_layout.addWidget(QLabel('磨皮强度 (0-1):'))
        self.smooth_input = QLineEdit('0.8')
        doubao_layout.addWidget(self.smooth_input)
        
        doubao_layout.addWidget(QLabel('美白强度 (0-1):'))
        self.whiten_input = QLineEdit('0.6')
        doubao_layout.addWidget(self.whiten_input)
        
        layout.addWidget(self.doubao_panel)
        
        # Banana parameters panel (hidden by default)
        self.banana_panel = QWidget()
        self.banana_panel.setVisible(False)
        banana_layout = QVBoxLayout(self.banana_panel)
        
        banana_layout.addWidget(QLabel('风格描述 Prompt:'))
        self.prompt_input = QLineEdit('convert to anime style, high detail')
        banana_layout.addWidget(self.prompt_input)
        
        layout.addWidget(self.banana_panel)
        
        # Separator
        self._add_separator(layout)
        
        # Output Directory
        output_label = QLabel('输出配置')
        output_label.setStyleSheet('font-weight: bold;')
        layout.addWidget(output_label)
        
        self.output_dir_btn = QPushButton('选择输出目录')
        self.output_dir_btn.clicked.connect(self.output_dir_clicked.emit)
        layout.addWidget(self.output_dir_btn)
        
        self.output_dir_label = QLabel('./output')
        self.output_dir_label.setWordWrap(True)
        self.output_dir_label.setStyleSheet('padding: 5px; background-color: #f5f5f5; border: 1px solid #ddd;')
        layout.addWidget(self.output_dir_label)
        
        # Spacer
        layout.addStretch()
        
        # Progress and Execution
        self.start_btn = QPushButton('启动批量处理')
        self.start_btn.setMinimumHeight(40)
        self.start_btn.clicked.connect(self.start_processing.emit)
        layout.addWidget(self.start_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
    
    def _add_separator(self, layout: QVBoxLayout):
        """Add a separator line to the layout."""
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
        layout.addSpacing(5)
    
    def _on_image_selected(self, row: int):
        """Handle image selection in list."""
        if 0 <= row < len(self.image_paths):
            pass  # Signal will be handled by parent
    
    def _on_model_changed(self, index: int):
        """Handle model selection change."""
        if index == 0:  # Doubao
            self.doubao_panel.setVisible(True)
            self.banana_panel.setVisible(False)
        else:  # Banana
            self.doubao_panel.setVisible(False)
            self.banana_panel.setVisible(True)
    
    def set_image_paths(self, paths: List[str]):
        """Update image list."""
        self.image_paths = paths
        self.image_list.clear()
        for path in paths:
            self.image_list.addItem(os.path.basename(path))
    
    def set_output_directory(self, path: str):
        """Set output directory label."""
        self.output_dir_label.setText(path)
    
    def get_current_model(self) -> str:
        """Get selected model type."""
        index = self.model_combo.currentIndex()
        return 'doubao' if index == 0 else 'banana'
    
    def get_model_params(self) -> Dict:
        """Get current model parameters."""
        model_type = self.get_current_model()
        
        if model_type == 'doubao':
            return {
                'edit_type': self.doubao_type_combo.currentText().split('(')[1].rstrip(')'),
                'smooth': float(self.smooth_input.text()),
                'whiten': float(self.whiten_input.text())
            }
        else:  # banana
            return {
                'prompt': self.prompt_input.text()
            }
    
    def set_progress(self, current: int, total: int):
        """Update progress bar."""
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        
        if current >= total:
            self.progress_bar.setVisible(False)
    
    def set_processing_enabled(self, enabled: bool):
        """Enable/disable start button during processing."""
        self.start_btn.setEnabled(enabled)
        self.import_btn.setEnabled(enabled)
    
    def get_selected_image_path(self) -> Optional[str]:
        """Get currently selected image path."""
        row = self.image_list.currentRow()
        if 0 <= row < len(self.image_paths):
            return self.image_paths[row]
        return None


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self.output_directory = './output'
        self.task_manager: Optional[TaskManager] = None
        
        self._init_ui()
        self._connect_signals()
    
    def _init_ui(self):
        self.setWindowTitle('AI 批量图片修改工具')
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with splitter
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left config panel (2/5 width)
        self.config_panel = ConfigPanel()
        splitter.addWidget(self.config_panel)
        splitter.setStretchFactor(0, 2)
        
        # Right preview panel (3/5 width)
        self.preview_panel = PreviewPanel()
        splitter.addWidget(self.preview_panel)
        splitter.setStretchFactor(1, 3)
        
        main_layout.addWidget(splitter)
    
    def _connect_signals(self):
        """Connect signals between components."""
        self.config_panel.import_clicked.connect(self._on_import_images)
        self.config_panel.api_config_clicked.connect(self._on_api_config)
        self.config_panel.output_dir_clicked.connect(self._on_select_output_dir)
        self.config_panel.start_processing.connect(self._on_start_processing)
        
        # Connect image list selection to preview
        self.config_panel.image_list.currentRowChanged.connect(
            lambda row: self._on_image_selected(row)
        )
    
    def _on_import_images(self):
        """Handle image import button click."""
        from PyQt6.QtWidgets import QFileDialog
        
        files, _ = QFileDialog.getOpenFileNames(
            self,
            '选择图片',
            '',
            '图片文件 (*.jpg *.jpeg *.png *.webp)'
        )
        
        if files:
            self.config_panel.set_image_paths(files)
            # Auto-select first image
            if files:
                self.config_panel.image_list.setCurrentRow(0)
    
    def _on_image_selected(self, row: int):
        """Handle image selection in list."""
        image_path = self.config_panel.get_selected_image_path()
        if image_path:
            self.preview_panel.set_original_image(image_path)
            self.preview_panel.clear_processed()
    
    def _on_api_config(self):
        """Handle API configuration button click."""
        config = self.config_manager.get_config()
        
        dialog = ApiConfigDialog(config, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Save configuration
            self.config_manager.save_to_env(dialog.result_config)
            QMessageBox.information(self, '配置已保存', 'API 配置已更新！')
    
    def _on_select_output_dir(self):
        """Handle output directory selection."""
        from PyQt6.QtWidgets import QFileDialog
        
        directory = QFileDialog.getExistingDirectory(
            self,
            '选择输出目录',
            self.output_directory
        )
        
        if directory:
            self.output_directory = directory
            self.config_panel.set_output_directory(directory)
    
    def _on_start_processing(self):
        """Handle start processing button click."""
        # Validation
        image_paths = self.config_panel.image_paths
        if not image_paths:
            QMessageBox.warning(self, '提示', '请先导入图片！')
            return
        
        # Check API configuration
        config = self.config_manager.get_config()
        model_type = self.config_panel.get_current_model()
        
        if model_type == 'doubao':
            if not config['doubao_api_url'] or not config['doubao_api_key']:
                QMessageBox.warning(self, '配置错误', '请先配置豆包 API！')
                return
        else:  # banana
            if not all([config['banana_api_url'], config['banana_api_key'], config['banana_model_key']]):
                QMessageBox.warning(self, '配置错误', '请先配置 Banana API！')
                return
        
        # Create output directory if not exists
        os.makedirs(self.output_directory, exist_ok=True)
        
        # Prepare tasks
        model_params = self.config_panel.get_model_params()
        tasks = [
            ProcessingTask(path, self.output_directory, model_type, model_params)
            for path in image_paths
        ]
        
        # Setup task manager
        self.task_manager = TaskManager(max_workers=5)
        self.task_manager.progress_update.connect(self.config_panel.set_progress)
        self.task_manager.task_completed.connect(self._on_task_completed)
        self.task_manager.all_completed.connect(self._on_all_completed)
        
        # Start processing
        self.config_panel.set_processing_enabled(False)
        self.task_manager.add_tasks(tasks)
        self.task_manager.start(config)
    
    def _on_task_completed(self, image_path: str, success: bool, error_message: str):
        """Handle task completion."""
        if success:
            # Find output path and update preview
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(self.output_directory, f"{base_name}_processed.png")
            
            # Update preview if this is the currently selected image
            current_selection = self.config_panel.get_selected_image_path()
            if current_selection == image_path:
                self.preview_panel.set_processed_image(output_path)
    
    def _on_all_completed(self, success_count: int, failure_count: int):
        """Handle all tasks completion."""
        self.config_panel.set_processing_enabled(True)
        
        message = f'处理完成！\n成功: {success_count}\n失败: {failure_count}'
        QMessageBox.information(self, '批量处理完成', message)
