import os
from pathlib import Path

# set default paths
DEFAULT_APP_DIR = Path(os.environ.get("FG_APP_DIR", "/app"))
DEFAULT_DATA_ROOT = Path(os.environ.get("FG_DATA_ROOT", "/fastgenomics"))
INPUT_FILE_MAPPING = os.environ.get("INPUT_FILE_MAPPING", None)

# summary key for the FGProcess.output
SUMMARY_KEY = "summary"
