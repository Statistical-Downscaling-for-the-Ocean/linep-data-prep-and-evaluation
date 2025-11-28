# config.py
import yaml
from importlib import resources


def load_config(cfg_file="CTD"):
    """
    Load the correct YAML config from the package.
    """

    try:
        with resources.open_text("linep_validator", cfg_file) as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"Could not find config file '{cfg_file}' inside the package. "
            f"Make sure your package is installed correctly."
        ) from e

    return cfg
