#!/usr/bin/env python3
"""
Example network operations script that demonstrates the use of the auto-retry decorator.
This script simulates common network operations that might fail and need retries.
"""

import sys
import random
import time
import argparse
import json
from typing import Dict, Any, Optional
from torero_decorators import ToreroAutoRetry

# Load decorator configuration from JSON schema
auto_retry = ToreroAutoRetry("auto-retry-deco.json")

# Simulated network operations
class NetworkDevice:
    def __init__(self, hostname: str, username: str, password: str):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.connected = False
    
    @auto_retry
    def connect(self) -> bool:
        """Simulate connecting to a network device with potential failures"""
        # Simulate connection issues (70% chance of failure)
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to connect to {self.hostname}")
        
        self.connected = True
        print(f"Successfully connected to {self.hostname}")
        return True
    
    @auto_retry
    def get_config(self) -> Dict[str, Any]:
        """Simulate retrieving device configuration with potential failures"""
        if not self.connected:
            raise ConnectionError(f"Not connected to {self.hostname}")
        
        # Simulate timeout issues (30% chance of failure)
        if random.random() < 0.3:
            raise TimeoutError(f"Timeout while retrieving config from {self.hostname}")
        
        return {
            "hostname": self.hostname,
            "interfaces": [
                {"name": "eth0", "status": "up", "ip": "192.168.1.1"},
                {"name": "eth1", "status": "down", "ip": "10.0.0.1"}
            ],
            "version": "1.0.0"
        }
    
    @auto_retry
    def apply_config(self, config: Dict[str, Any]) -> bool:
        """Simulate applying configuration with potential failures"""
        if not self.connected:
            raise ConnectionError(f"Not connected to {self.hostname}")
        
        # Simulate configuration issues (40% chance of failure)
        if random.random() < 0.4:
            raise Exception(f"Failed to apply configuration to {self.hostname}")
        
        print(f"Successfully applied configuration to {self.hostname}")
        return True
    
    def disconnect(self) -> None:
        """Disconnect from the device"""
        if self.connected:
            print(f"Disconnected from {self.hostname}")
            self.connected = False

def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Network Operations Example with Auto-Retry")
    parser.add_argument("--hostname", required=True, help="Device hostname")
    parser.add_argument("--username", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")
    parser.add_argument("--operation", choices=["connect", "get-config", "apply-config"], 
                        required=True, help="Operation to perform")
    
    # Add decorator configuration options
    parser.add_argument("--max-retries", type=int, help="Maximum number of retry attempts")
    parser.add_argument("--delay", type=float, help="Initial delay between retries in seconds")
    parser.add_argument("--backoff-factor", type=float, help="Multiplier for delay after each retry")
    
    return parser.parse_args()

def main() -> int:
    """Main function"""
    args = parse_args()
    
    # Update decorator configuration if provided
    config = {}
    if args.max_retries:
        config["max_retries"] = args.max_retries
    if args.delay:
        config["delay"] = args.delay
    if args.backoff_factor:
        config["backoff_factor"] = args.backoff_factor
    
    if config:
        auto_retry.update_config(config)
    
    # Create device instance
    device = NetworkDevice(args.hostname, args.username, args.password)
    
    try:
        # Connect to device
        device.connect()
        
        # Perform requested operation
        if args.operation == "get-config":
            config = device.get_config()
            print(f"Device configuration: {config}")
        elif args.operation == "apply-config":
            # Example configuration to apply
            config = {
                "interfaces": [
                    {"name": "eth0", "ip": "192.168.1.2"}
                ]
            }
            device.apply_config(config)
        
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    finally:
        device.disconnect()

if __name__ == "__main__":
    sys.exit(main()) 