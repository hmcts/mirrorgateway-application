import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

INCOMING_DIR = os.environ.get("INCOMING_DIR", "")
ARCHIVE_DIR = os.environ.get("ARCHIVE_DIR", "")
STATUS_DIR = os.path.join(INCOMING_DIR, "receipts")

LOG_DIR = os.environ.get("LOG_DIR", "")

CASE_SCHEMA_PATH = os.path.join(ROOT_DIR, "schemas", "SendCaseSJP.xsd")
RESULT_SCHEMA_PATH = os.path.join(ROOT_DIR, "schemas", "SendResults.xsd")

API_USERNAME = os.environ.get("API_USERNAME", "")
API_PASSWORD = os.environ.get("API_PASSWORD", "")
API_ENDPOINT = os.environ.get("API_ENDPOINT", "")

EMAIL_FROM = os.environ.get("STATUS_EMAIL_FROM", "")
EMAIL_TO = os.environ.get("STATUS_EMAIL_TO", "")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
AWS_ACCESS_KEY_SECRET = os.environ.get("AWS_SECRET_ACCESS_KEY", None)

ARCHIVE_PROCESSED_FILES = os.environ.get("ARCHIVE_PROCESSED_FILES", "False") == "True"

GPG_HOME_DIRECTORY = os.environ.get("GPG_HOME_DIRECTORY", "")
GPG_RECIPIENT = os.environ.get("GPG_RECIPIENT", "")

ENCRYPT_ARCHIVE_DATA = True

RELEASE_STAGE = os.environ.get("RELEASE_STAGE", "")

CREATE_STATUS_FILES = os.environ.get("CREATE_STATUS_FILES", "False") == "True"

MANUAL_RUN = False

try:
    from .local import *
except ImportError:
    pass
