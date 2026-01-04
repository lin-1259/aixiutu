import base64
import requests
from io import BytesIO
from PIL import Image
from typing import Dict, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DoubaoClient:
    """Client for Doubao (豆包) image editing API."""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
    
    def edit_image(self, image_base64: str, edit_type: str, 
                   smooth: float, whiten: float, timeout: int = 60) -> Tuple[bool, Optional[str], Optional[bytes]]:
        """
        Edit image using Doubao API.
        
        Args:
            image_base64: Base64 encoded image
            edit_type: 'retouch' or 'enhance'
            smooth: Smoothing strength (0-1)
            whiten: Whitening strength (0-1)
            timeout: Request timeout in seconds
            
        Returns:
            Tuple of (success, error_message, image_bytes)
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'image': image_base64,
                'edit_type': edit_type,
                'smooth': smooth,
                'whiten': whiten
            }
            
            logger.info(f"Sending request to Doubao API: {self.api_url}")
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            result = response.json()
            
            if 'image' in result:
                result_base64 = result['image']
                image_bytes = base64.b64decode(result_base64)
                return True, None, image_bytes
            else:
                return False, 'API response missing image data', None
                
        except requests.exceptions.Timeout:
            error_msg = f'Doubao API request timeout after {timeout}s'
            logger.error(error_msg)
            return False, error_msg, None
        except requests.exceptions.RequestException as e:
            error_msg = f'Doubao API request failed: {str(e)}'
            logger.error(error_msg)
            return False, error_msg, None
        except Exception as e:
            error_msg = f'Doubao processing error: {str(e)}'
            logger.error(error_msg)
            return False, error_msg, None


class BananaClient:
    """Client for Banana style transfer API."""
    
    def __init__(self, api_url: str, api_key: str, model_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.model_key = model_key
    
    def apply_style(self, image_base64: str, prompt: str, timeout: int = 60) -> Tuple[bool, Optional[str], Optional[bytes]]:
        """
        Apply style to image using Banana API.
        
        Args:
            image_base64: Base64 encoded image
            prompt: Style description prompt
            timeout: Request timeout in seconds
            
        Returns:
            Tuple of (success, error_message, image_bytes)
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'image': image_base64,
                'model_key': self.model_key,
                'prompt': prompt
            }
            
            logger.info(f"Sending request to Banana API: {self.api_url}")
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            result = response.json()
            
            if 'image' in result:
                result_base64 = result['image']
                image_bytes = base64.b64decode(result_base64)
                return True, None, image_bytes
            else:
                return False, 'API response missing image data', None
                
        except requests.exceptions.Timeout:
            error_msg = f'Banana API request timeout after {timeout}s'
            logger.error(error_msg)
            return False, error_msg, None
        except requests.exceptions.RequestException as e:
            error_msg = f'Banana API request failed: {str(e)}'
            logger.error(error_msg)
            return False, error_msg, None
        except Exception as e:
            error_msg = f'Banana processing error: {str(e)}'
            logger.error(error_msg)
            return False, error_msg, None


def image_to_base64(image_path: str) -> str:
    """Convert image file to base64 string (PNG format)."""
    try:
        with Image.open(image_path) as img:
            # Convert to PNG format for consistency
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()
            return base64.b64encode(image_bytes).decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to convert image to base64: {str(e)}")
        raise
