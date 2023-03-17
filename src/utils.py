from pathlib import Path

import yaml

DATA_PATH = Path("../data/")
CONFIG_PATH = DATA_PATH / "config.yaml"

with open(CONFIG_PATH, mode="r") as fp:
    config = yaml.safe_load(fp)

