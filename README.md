# Torero Auto-Retry Decorator Example

This repository demonstrates a simplified auto-retry decorator implementation for network automation tasks using Torero. The decorator automatically retries failed operations with exponential backoff.

## Overview

The auto-retry decorator provides a simple way to handle transient failures in network operations by:
- Automatically retrying failed operations
- Implementing exponential backoff
- Providing detailed logging of retry attempts
- Simulating network operations with configurable success rates

## Project Structure

```
torero-resources/
├── network-scripts/
│   ├── main.py              # Main script with simulated operations
│   ├── torero_decorators.py # Auto-retry decorator implementation
│   ├── auto-retry-deco.json # Decorator schema
│   └── requirements.txt     # Project dependencies
└── network-operations.json  # Service configuration
```

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/ArishIT/torero_prototype.git
cd torero_prototype
```

2. Install dependencies:
```bash
pip install -r torero-resources/network-scripts/requirements.txt
```

3. Make sure you have Torero CLI installed and configured:
```bash
pip install torero
torero configure  # Follow the prompts to set up your environment
```

## Quick Start

1. Create the service:
```bash
torero create service python-script network-operations --filename main.py --working-dir network-scripts
```

2. Run the service:
```bash
torero run service python-script network-operations
```

The service will attempt three operations (connect, get-config, apply-config) with a 70% success rate for each. Failed operations will be retried automatically.

## Configuration

The auto-retry decorator supports the following parameters (defined in `auto-retry-deco.json`):

- `max-retries`: Maximum number of retry attempts (default: 3)
- `delay`: Initial delay between retries in seconds (default: 1.0)
- `backoff-factor`: Multiplier for delay after each retry (default: 2.0)

## Example Output

```
2025-04-03 15:51:51 - WARNING - Attempt 1/3 failed: Operation connect failed. Retrying in 1.0 seconds...
2025-04-03 15:51:52 - WARNING - Attempt 2/3 failed: Operation connect failed. Retrying in 2.0 seconds...
Successfully completed connect
Successfully completed get-config
Operation apply-config failed after all retries
```

## Benefits

- **Simplified Error Handling**: Automatically handle transient failures
- **Configurable Retry Logic**: Customize retry behavior through parameters
- **Clear Logging**: Track retry attempts and failures for debugging
- **Easy Integration**: Simple decorator-based approach

## Dependencies

Required Python packages:
- torero
- requests>=2.31.0
- urllib3>=2.0.7

## Extending the Decorator

You can extend the auto-retry decorator by:

1. Adding more configuration options to the JSON schema
2. Implementing additional retry strategies
3. Adding support for more exception types
4. Integrating with external monitoring or alerting systems 
