# Torero Auto-Retry Decorator Example

This repository demonstrates how to use the auto-retry decorator with Torero to handle common network automation tasks with automatic retry functionality.

## Overview

The auto-retry decorator provides a simple way to add retry logic to network automation scripts. It's designed to work with Torero's decorator system and can be attached to any service. This implementation helps handle transient network issues by automatically retrying failed operations with configurable parameters.

## Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher installed
- Git installed
- Access to a network device for testing
- Basic understanding of network automation concepts

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

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ArishIT/torero_prototype.git
cd torero_prototype
```

2. Install the required dependencies:
```bash
python3 -m pip install -r torero-resources/network-scripts/requirements.txt
```

3. Configure Torero (if not already configured):
```bash
torero configure
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

## Configuration

The auto-retry decorator supports the following parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| max-retries | integer | 3 | Maximum number of retry attempts |
| delay | number | 1.0 | Initial delay between retries in seconds |
| backoff-factor | number | 2.0 | Multiplier for delay after each retry |

## Benefits

- **Simplified Error Handling**: Automatically retry operations that might fail due to temporary issues
- **Configurable Retry Logic**: Adjust retry parameters based on your specific needs
- **Consistent Behavior**: Apply the same retry logic across different network automation scripts
- **Detailed Logging**: Track retry attempts and failures for debugging

## Dependencies

The project requires the following Python packages:
- `requests>=2.31.0`
- `urllib3>=2.0.7`

## Troubleshooting

Common issues and solutions:

1. **ImportError: No module named 'torero'**
   - Ensure you have installed all dependencies from requirements.txt
   - Check if Python is in your PATH
   - Try using `python3 -m pip install` instead of just `pip`

2. **Permission Denied Errors**
   - Ensure you have the necessary permissions to access network devices
   - Check if your credentials are correctly configured

3. **Retry Logic Not Working**
   - Verify that the decorator is properly attached to your service
   - Check the auto-retry-deco.json configuration
   - Ensure the max-retries parameter is set appropriately

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 