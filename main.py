import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import logging

from config_manager import ConfigManager
from ui_components import MainWindow

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the AI Batch Image Editor."""
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName('AI 批量图片修改工具')
    app.setOrganizationName('AI Image Tools')
    
    # Enable high DPI scaling
    app.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Initialize configuration manager
    config_manager = ConfigManager()
    
    # Create and show main window
    window = MainWindow(config_manager)
    window.show()
    
    logger.info('Application started')
    
    # Run application
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
