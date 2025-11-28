import yaml
import importlib.resources


def load_config(filename="config_CTD.yaml"):
    """
    Load the packaged config.yaml from the linep_validator package.
    """
    with importlib.resources.open_text("linep_validator", filename) as f:
        return yaml.safe_load(f)
