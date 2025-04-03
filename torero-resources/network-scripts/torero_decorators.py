#!/usr/bin/env python3
"""
Implementation of the auto-retry decorator for Torero services.
"""

import time
import logging
from functools import wraps
from typing import Callable, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('torero_decorators')

def autoretry(max_retries=3, delay=1.0, backoff_factor=2.0):
    """
    Decorator that automatically retries a function when it fails.
    
    Args:
        max_retries (int): Maximum number of retry attempts
        delay (float): Initial delay between retries in seconds
        backoff_factor (float): Multiplier for delay after each retry
    """
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