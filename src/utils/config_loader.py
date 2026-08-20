import os
import yaml

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_CONFIG_PATH = os.path.join(_PROJECT_ROOT, "config", "config.yaml")

_config_cache = None


def load_config():
    global _config_cache
    if _config_cache is None:
        with open(_CONFIG_PATH, "r") as f:
            _config_cache = yaml.safe_load(f)
    return _config_cache


def resolve_path(relative_path):
    return os.path.join(_PROJECT_ROOT, relative_path)
