# Torero Auto-Retry Decorator Example

This repository demonstrates how to use the auto-retry decorator with Torero to handle common network automation tasks with automatic retry functionality.

## Overview

The auto-retry decorator provides a simple way to add retry logic to network automation scripts. It's designed to work with Torero's decorator system and can be attached to any service.

## Project Structure

```
torero-resources/
├── network-scripts/
│   ├── main.py                 # Main network operations script with retry functionality
│   ├── requirements.txt        # Python dependencies
│   ├── auto-retry-deco.json    # JSON schema definition for the decorator
│   └── torero_decorators.py    # Python implementation of the auto-retry decorator
└── network-operations.json     # Service configuration file
```

## Setup with Torero

### 1. Create a Repository

First, create a repository in Torero to store your scripts:

```bash
torero create repository network-operations-repo --url file:///path/to/torero-resources
```

### 2. Create the Decorator

Create the auto-retry decorator in Torero using the JSON schema:

```bash
torero create decorator auto-retry --schema @./network-scripts/auto-retry-deco.json
```

### 3. Create a Python Script Service

Create a service for the network operations script:

```bash
torero create service python-script network-operations --repository network-operations-repo --filename main.py --working-dir network-scripts --description "Network operations with auto-retry functionality"
```

## Running the Service

You can run the service with various parameters:

```bash
# Basic usage
torero run service python-script network-operations --set hostname=router1 --set username=admin --set password=secret --set operation=connect

# With retry configuration
torero run service python-script network-operations --set hostname=router1 --set username=admin --set password=secret --set operation=connect --set max-retries=3 --set delay=1.0 --set backoff-factor=2.0
```

## Available Operations

The service supports the following operations:

- `connect`: Attempt to connect to a network device
- `get-config`: Retrieve device configuration
- `apply-config`: Apply configuration to the device

## Retry Configuration Options

The auto-retry decorator supports the following configuration options:

- `max-retries`: Maximum number of retry attempts (default: 3)
- `delay`: Initial delay between retries in seconds (default: 1.0)
- `backoff-factor`: Multiplier for delay after each retry (default: 2.0)

## Example Output

When running the service, you'll see output like:

```
2025-04-03 15:23:43,904 - torero_decorators - WARNING - Attempt 1/3 failed for connect. Error: Failed to connect to router1. Retrying in 1.0 seconds...
2025-04-03 15:23:44,904 - torero_decorators - INFO - Successfully connected to router1
Operation completed successfully: True
```

## Benefits

- **Simplified Error Handling**: Automatically retry operations that might fail due to temporary issues
- **Configurable Retry Logic**: Adjust retry parameters based on your specific needs
- **Consistent Behavior**: Apply the same retry logic across different network automation scripts
- **Detailed Logging**: Track retry attempts and failures for debugging

## Dependencies

The project requires the following Python packages:
- `torero`
- `requests>=2.31.0`
- `urllib3>=2.0.7`

## Extending the Decorator

You can extend the auto-retry decorator by:

1. Adding more configuration options to the JSON schema
2. Implementing additional retry strategies
3. Adding support for more exception types
4. Integrating with external monitoring or alerting systems 