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

# Load decorator configuration
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
                {"name": "eth1", "status": "down", "ip": "192.168.2.1"}
            ]
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

def main():
    parser = argparse.ArgumentParser(description="Network operations with auto-retry functionality")
    parser.add_argument('--hostname', required=True, help="Device hostname to connect to")
    parser.add_argument('--username', required=True, help="Username for device authentication")
    parser.add_argument('--password', required=True, help="Password for device authentication")
    parser.add_argument('--operation', required=True, choices=['connect', 'get-config', 'apply-config'],
                      help="Operation to perform on the device")
    parser.add_argument('--max-retries', type=int, default=3, help="Maximum number of retry attempts")
    parser.add_argument('--delay', type=float, default=1.0, help="Initial delay between retries in seconds")
    parser.add_argument('--backoff-factor', type=float, default=2.0, help="Multiplier for delay after each retry")
    
    args = parser.parse_args()
    
    # Create device instance
    device = NetworkDevice(args.hostname, args.username, args.password)
    
    # Perform requested operation
    if args.operation == 'connect':
        result = device.connect()
    elif args.operation == 'get-config':
        result = device.get_config()
    elif args.operation == 'apply-config':
        # Example configuration to apply
        config = {
            "interfaces": [
                {"name": "eth0", "ip": "192.168.1.2"}
            ]
        }
        result = device.apply_config(config)
    else:
        print(f"Operation {args.operation} not implemented")
        sys.exit(1)
    
    print(f"Operation completed successfully: {result}")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 