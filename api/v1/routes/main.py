import os
import argparse
import logging
import json
import sys

from core_engine import config
from core_engine.utils import setup_logging, load_module
from core_engine.exceptions import ConfigurationError, ModuleLoadError

def main():
    """
    Main entry point for the core-engine application.
    Handles argument parsing, configuration loading, and module execution.
    """
    parser = argparse.ArgumentParser(description="Core Engine Application")
    parser.add_argument("-c", "--config", dest="config_path",
                        default="config.json", help="Path to the configuration file")
    parser.add_argument("-m", "--module", dest="module_name",
                        required=True, help="Name of the module to execute")
    parser.add_argument("-v", "--verbosity", dest="verbosity",
                        default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Logging verbosity level")

    args = parser.parse_args()

    try:
        setup_logging(level=args.verbosity)

        # Load configuration
        try:
            with open(args.config_path, "r") as f:
                cfg = json.load(f)
                config.set_config(cfg)  # Set global configuration
        except FileNotFoundError as e:
            raise ConfigurationError(f"Configuration file not found: {args.config_path}") from e
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {args.config_path}") from e
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}") from e

        # Load and execute the module
        try:
            module = load_module(args.module_name)
            if hasattr(module, "run") and callable(module.run):
                module.run()
            else:
                logging.error(f"Module '{args.module_name}' does not have a 'run' function.")
                sys.exit(1) # Exit with an error code

        except ModuleLoadError as e:
            logging.error(f"Failed to load module '{args.module_name}': {e}")
            sys.exit(1) # Exit with an error code
        except Exception as e:
            logging.exception(f"An unexpected error occurred during module execution: {e}")
            sys.exit(1) # Exit with an error code

    except ConfigurationError as e:
        logging.error(f"Configuration error: {e}")
        sys.exit(1) #Exit with an error code
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        sys.exit(1) # Exit with an error code

if __name__ == "__main__":
    main()