import os
from dotenv import load_dotenv
from typing import Dict, Optional


class ConfigManager:
    """Manages API configuration loading and saving."""
    
    def __init__(self):
        self.config = {
            'doubao_api_url': '',
            'doubao_api_key': '',
            'banana_api_url': '',
            'banana_api_key': '',
            'banana_model_key': ''
        }
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from .env file."""
        load_dotenv()
        
        self.config['doubao_api_url'] = os.getenv('DOUBAO_API_URL', '')
        self.config['doubao_api_key'] = os.getenv('DOUBAO_API_KEY', '')
        self.config['banana_api_url'] = os.getenv('BANANA_API_URL', '')
        self.config['banana_api_key'] = os.getenv('BANANA_API_KEY', '')
        self.config['banana_model_key'] = os.getenv('BANANA_MODEL_KEY', '')
    
    def update_config(self, config_dict: Dict[str, str]):
        """Update configuration from dictionary."""
        self.config.update(config_dict)
    
    def get_config(self) -> Dict[str, str]:
        """Get current configuration."""
        return self.config.copy()
    
    def save_to_env(self, config_dict: Dict[str, str]):
        """Save configuration to .env file."""
        env_content = """# AI Batch Image Editor - API Configuration

# Doubao (豆包) API Configuration
DOUBAO_API_URL={doubao_api_url}
DOUBAO_API_KEY={doubao_api_key}

# Banana API Configuration
BANANA_API_URL={banana_api_url}
BANANA_API_KEY={banana_api_key}
BANANA_MODEL_KEY={banana_model_key}
""".format(**config_dict)
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        self.update_config(config_dict)
