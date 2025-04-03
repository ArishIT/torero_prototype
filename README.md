# Torero Auto-Retry Decorator Example

This repository demonstrates how to use the auto-retry decorator with Torero to handle common network automation tasks with automatic retry functionality.

## Overview

The auto-retry decorator provides a simple way to add retry logic to network automation scripts. It's designed to work with Torero's decorator system and can be attached to any service. This implementation helps handle transient network issues by automatically retrying failed operations with configurable parameters.

## Project Structure

```
torero-resources/
├── README.md                 # Project documentation
├── network-scripts/          # Main implementation directory
│   ├── main.py              # Example script with auto-retry implementation
│   ├── torero_decorators.py # Decorator implementation
│   ├── auto-retry-deco.json # Configuration for retry behavior
│   └── requirements.txt     # Project dependencies (none required)
└── .git/                    # Git repository information
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ArishIT/torero_prototype.git
cd torero_prototype
```

2. No additional dependencies are required as the project uses only Python standard library modules.

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

- **Simplicity**: Uses only Python standard library modules
- **Flexibility**: Configurable retry parameters through JSON schema
- **Reliability**: Automatic handling of transient failures
- **Transparency**: Detailed logging of retry attempts and outcomes

## Implementation Details

The project consists of two main components:

1. **Auto-Retry Decorator** (`torero_decorators.py`):
   - Implements the retry logic
   - Configurable through JSON schema
   - Provides detailed logging

2. **Example Script** (`main.py`):
   - Demonstrates decorator usage
   - Simulates network operations
   - Shows retry behavior in action

## Contributing

Feel free to submit issues and enhancement requests!
