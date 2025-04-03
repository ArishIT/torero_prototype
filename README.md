# Torero Auto-Retry Decorator Example

This repository demonstrates how to use the auto-retry decorator with Torero to handle common network automation tasks with automatic retry functionality.

## Overview

The auto-retry decorator provides a simple way to add retry logic to network automation scripts. It's designed to work with Torero's decorator system and can be attached to any service.

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

You can run the service with a simple command:

```bash
torero run service python-script network-operations
```

The script will:
1. Try each operation (connect, get-config, apply-config)
2. Each operation has a 70% chance of success
3. If an operation fails, it will retry up to 3 times with increasing delays
4. You'll see the results in the output

## Example Output

When running the service, you'll see output like:

```
2025-04-03 15:23:43,904 - torero_decorators - WARNING - Attempt 1/3 failed for connect. Error: Operation connect failed. Retrying in 1.0 seconds...
2025-04-03 15:23:44,904 - torero_decorators - INFO - Successfully completed connect
Successfully completed get-config
Successfully completed apply-config
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
