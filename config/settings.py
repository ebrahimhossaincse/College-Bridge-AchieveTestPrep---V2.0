import yaml
from config.base_config import BaseConfig

ENV = BaseConfig.ENV
HEADLESS = BaseConfig.HEADLESS
BROWSER = BaseConfig.BROWSER

try:
    yaml_path = BaseConfig.ENV_CONFIG_DIR / f"{ENV}.yaml"
    with open(yaml_path, "r") as file:
        config_data = yaml.safe_load(file)
        BASE_URL = config_data.get("college_bridge_url")
        print(f"[INFO] Loaded BASE_URL from {yaml_path}: {BASE_URL}")
except FileNotFoundError:
    print(f"[ERROR] {ENV}.yaml file not found in config/environments.")
    BASE_URL = None
