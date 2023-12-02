# pulpo-config

[![Python package](https://github.com/jasonray/pulpo-config/actions/workflows/python-package.yml/badge.svg)](https://github.com/jasonray/pulpo-config/actions/workflows/python-package.yml) 
[![PyPI version](https://badge.fury.io/py/pulpo-config.svg)](https://badge.fury.io/py/pulpo-config)

# Overview
The `Config` class provides a robust and flexible way to manage configuration settings in Python applications. It offers a simple interface to load, retrieve, and set configuration parameters, making it ideal for projects that require dynamic configuration handling.

# Key Features
## Easy Initialization
* Initialize with a dictionary of options or a JSON file.
* Automatically loads options from a file if a file path is provided.
## Flexible Option Retrieval
* Retrieve configuration values with support for nested keys.
* Environment variable substitution for values starting with `$ENV`.
## Command-Line Argument Processing
* Seamlessly integrates with `argparse` to update configurations from command-line arguments.
* Accepts arguments as a dictionary or `argparse.Namespace` object.
## JSON and String Representation
* Convert configurations to a JSON string or a standard string representation for easy debugging and logging.
## Specialized Value Retrieval
* Get configuration values as boolean or integer types with `getAsBool` and `getAsInt`.
* Handles type conversion and validation internally.
## Dynamic Configuration Setting
* Set configuration values with support for nested keys.
* Automatically creates intermediate dictionaries if needed.
# Benefits
* `Flexibility`: Easily manage configurations with varying levels of complexity.
* `Simplicity`: Streamline configuration management without extensive boilerplate code.
* `Compatibility`: Works seamlessly with common Python libraries like `argparse`.
* `Extensibility`: Customize and extend for more complex use cases or specific project needs.

# Example Usage
``` python
from pulpo_config import Config

# Can load values manually through a dictionary..
config = Config(options={"database": {"host": "localhost", "port": 3306}})

# Or can load values manually..
config.set("api_key", "your-api-key")
config.set('database.host', 'localhost')

# Or can load options from a JSON config file
config = Config(json_file_path="config.json")

# Or can load from command line parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--debug_mode', type=str)
config.process_args(parser)

# Retrieve a simple configuration value
api_key = config.get("api_key")

# Retrieve a simple configuration value
is_debug_mode = config.getAsBool("debug_mode")

# Retrieve a nested configuration value
db_host = config.get("database.host")
```
