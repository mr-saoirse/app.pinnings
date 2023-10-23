from loguru import logger
from pathlib import Path
import apin

HOME = Path(apin.__file__).parent.parent
STACK_HOME = f"{HOME}/stack"
APPS_HOME = f"{STACK_HOME}/application-sets"
