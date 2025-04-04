#!/usr/bin/env python3
"""
Example network operations script that demonstrates the use of the auto-retry decorator.
This script simulates common network operations that might fail and need retries.
"""

import random
from torero_decorators import autoretry

@autoretry()
def simulate_operation(operation):
    """Simulate a network operation that may fail"""
    # Simulate operation attempt with 30% chance of failure
    if random.random() < 0.7:  # 70% chance of success
        return f"Successfully completed {operation}"
    raise ConnectionError(f"Operation {operation} failed")

def main():
    """Main function to demonstrate auto-retry functionality"""
    operations = ["connect", "get-config", "apply-config"]
    
    for operation in operations:
        try:
            result = simulate_operation(operation)
            print(result)
        except Exception as e:
            print(f"Operation {operation} failed after all retries: {str(e)}")

if __name__ == "__main__":
    main() 