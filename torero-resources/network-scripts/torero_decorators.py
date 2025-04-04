#!/usr/bin/env python3
"""
Implementation of the auto-retry decorator for Torero services.
"""

import time
import logging
import json
from functools import wraps
from typing import Callable, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('torero_decorators')

def load_config(config_path: str = "auto-retry-deco.json") -> Dict[str, Any]:
    """
    Load configuration from JSON file.
    
    Args:
        config_path (str): Path to the JSON configuration file
        
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config['properties']

def autoretry(config_path: str = "auto-retry-deco.json"):
    """
    Decorator that automatically retries a function when it fails.
    Configuration is loaded from a JSON file.
    
    Args:
        config_path (str): Path to the JSON configuration file
    """
    config = load_config(config_path)
    max_retries = config['max-retries']['default']
    delay = config['delay']['default']
    backoff_factor = config['backoff-factor']['default']
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        logger.error(f"Operation failed after {max_retries} attempts: {str(e)}")
                        raise e
                    
                    logger.warning(f"Attempt {retries}/{max_retries} failed: {str(e)}. Retrying in {current_delay} seconds...")
                    time.sleep(current_delay)
                    current_delay *= backoff_factor
            
            return None
        return wrapper
    return decorator 