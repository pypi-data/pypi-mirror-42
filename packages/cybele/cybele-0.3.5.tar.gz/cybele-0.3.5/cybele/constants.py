import os


try:
    USER_NAME = os.getlogin()
except OSError as exc:
    USER_NAME = "default"

USER_HOME = os.path.expanduser("~")
CYBELE_DIRNAME = ".cybele"
DEFAULT_DB_PATH = os.path.join(USER_HOME, CYBELE_DIRNAME, f"{USER_NAME}.cybeledb")
