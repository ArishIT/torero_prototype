# Torero Auto-Retry Decorator Example

This repository demonstrates how to use the auto-retry decorator with Torero to handle common network automation tasks with automatic retry functionality.

## Overview

The auto-retry decorator provides a simple way to add retry logic to network automation scripts. It's designed to work with Torero's decorator system and can be attached to any service.

## Files

- `auto-retry-deco.json`: JSON schema definition for the decorator
- `torero_decorators.py`: Python implementation of the auto-retry decorator
- `network_operations.py`: Example script without retry functionality
- `network_operations_with_retry.py`: Example script with retry functionality

## Setup with Torero

### 1. Create a Repository

First, create a repository in Torero to store your scripts:

```bash
torero create repository network-automation-repo --description "Network automation scripts with auto-retry decorator" --url https://github.com/yourusername/network-automation-repo.git --reference main
```

### 2. Create the Decorator

Create the auto-retry decorator in Torero using the JSON schema:

```bash
torero create decorator auto-retry --schema @./auto-retry-deco.json
```

### 3. Create a Python Script Service

Create a service for the network operations script:

```bash
torero create service python-script network-operations --repository network-automation-repo --filename network_operations_with_retry.py --description "Network operations with auto-retry functionality"
```

### 4. Attach the Decorator to the Service

Attach the auto-retry decorator to the service:

```bash
torero attach-decorator auto-retry --service network-operations
```

## Running the Service

You can run the service with various parameters:

```bash
# Basic usage
torero run service python-script network-operations --set hostname=router1 --set username=admin --set password=secret --set operation=connect

# With decorator configuration
torero run service python-script network-operations --set hostname=router1 --set username=admin --set password=secret --set operation=connect --set max-retries=5 --set delay=2.0
```

## Decorator Configuration Options

The auto-retry decorator supports the following configuration options:

- `max_retries`: Maximum number of retry attempts (default: 3)
- `delay`: Initial delay between retries in seconds (default: 1.0)
- `backoff_factor`: Multiplier for delay after each retry (default: 2.0)
- `exceptions`: List of exception types to catch and retry on (default: ["ConnectionError", "TimeoutError"])

## Example Output

When running the service, you'll see output like:

```
2023-06-01 12:34:56,789 - torero_decorators - WARNING - Attempt 1/3 failed for connect. Error: Failed to connect to router1. Retrying in 1.0 seconds...
2023-06-01 12:34:57,789 - torero_decorators - WARNING - Attempt 2/3 failed for connect. Error: Failed to connect to router1. Retrying in 2.0 seconds...
2023-06-01 12:34:59,789 - torero_decorators - INFO - Successfully connected to router1
```

## Benefits

- **Simplified Error Handling**: Automatically retry operations that might fail due to temporary issues
- **Configurable Retry Logic**: Adjust retry parameters based on your specific needs
- **Consistent Behavior**: Apply the same retry logic across different network automation scripts
- **Detailed Logging**: Track retry attempts and failures for debugging

## Extending the Decorator

You can extend the auto-retry decorator by:

1. Adding more configuration options to the JSON schema
2. Implementing additional retry strategies
3. Adding support for more exception types
4. Integrating with external monitoring or alerting systems 