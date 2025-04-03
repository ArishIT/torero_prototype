import time
import logging
import json
from functools import wraps
from typing import Callable, Type, Union, Tuple, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('torero_decorators')

class ToreroAutoRetry:
    """
    Torero decorator for automatic retry functionality.
    This decorator can be attached to services using the Torero CLI.
    """
    
    def __init__(self, config_path: str = "auto-retry-deco.json"):
        """
        Initialize the decorator with configuration from JSON schema.
        
        Args:
            config_path (str): Path to the JSON schema configuration file
        """
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Set default values from schema
        self.max_retries = self.config['properties']['max_retries']['default']
        self.delay = self.config['properties']['delay']['default']
        self.backoff_factor = self.config['properties']['backoff_factor']['default']
        self.exceptions = tuple(eval(exc) for exc in self.config['properties']['exceptions']['default'])
    
    def __call__(self, func: Callable) -> Callable:
        """
        Decorator implementation that adds retry logic to the decorated function.
        
        Args:
            func (Callable): The function to decorate
            
        Returns:
            Callable: The decorated function with retry logic
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = self.delay
            last_exception = None
            
            for attempt in range(self.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except self.exceptions as e:
                    last_exception = e
                    if attempt == self.max_retries:
                        logger.error(
                            f"Function {func.__name__} failed after {self.max_retries} retries. "
                            f"Last error: {str(e)}"
                        )
                        raise
                    
                    logger.warning(
                        f"Attempt {attempt + 1}/{self.max_retries} failed for {func.__name__}. "
                        f"Error: {str(e)}. Retrying in {current_delay} seconds..."
                    )
                    
                    time.sleep(current_delay)
                    current_delay *= self.backoff_factor
            
            raise last_exception
        
        return wrapper
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """
        Update the decorator configuration with new values.
        
        Args:
            config (Dict[str, Any]): New configuration values
        """
        if 'max_retries' in config:
            self.max_retries = config['max_retries']
        if 'delay' in config:
            self.delay = config['delay']
        if 'backoff_factor' in config:
            self.backoff_factor = config['backoff_factor']
        if 'exceptions' in config:
            self.exceptions = tuple(eval(exc) for exc in config['exceptions'])

# Example usage
if __name__ == "__main__":
    # Create decorator instance
    auto_retry = ToreroAutoRetry()
    
    # Example function that might fail
    @auto_retry
    def example_network_operation():
        # Simulate a network operation that might fail
        import random
        if random.random() < 0.7:  # 70% chance of failure
            raise ConnectionError("Failed to connect to network device")
        return "Operation successful!"
    
    # Test the decorator
    try:
        result = example_network_operation()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Final error: {e}") 