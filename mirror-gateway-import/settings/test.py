import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TEST_FILE_DIRECTORY = os.path.join(ROOT_DIR, "test")

TEST_DATA_FILES = os.path.join(TEST_FILE_DIRECTORY, "test_data_files")

INCOMING_DIR = os.path.join(ROOT_DIR, TEST_FILE_DIRECTORY, "incoming")
ARCHIVE_DIR = os.path.join(ROOT_DIR, TEST_FILE_DIRECTORY, "archive")
STATUS_DIR = os.path.join(ROOT_DIR, TEST_FILE_DIRECTORY, "receipts")

LOG_DIR = os.path.join(ROOT_DIR, TEST_FILE_DIRECTORY, "logs")

CASE_SCHEMA_PATH = os.path.join(ROOT_DIR, "schemas", "SendCase.xsd")
RESULT_SCHEMA_PATH = os.path.join(ROOT_DIR, "schemas", "SendResults.xsd")

API_USERNAME = "test_username"
API_PASSWORD = "test_password"
API_ENDPOINT = "http://whatever.com/api/"

EMAIL_FROM = ["DX data import script", "test@test.com"]
EMAIL_TO = "test@test.com"

AWS_ACCESS_KEY_ID = "testing"
AWS_ACCESS_KEY_SECRET = "testing"

ARCHIVE_PROCESSED_FILES = False

GPG_HOME_DIRECTORY = os.environ.get("gpg_home_directory", "")
GPG_RECIPIENT = os.environ.get("gpg_recipient", "")

ENCRYPT_ARCHIVE_DATA = False

CREATE_STATUS_FILES = True

MANUAL_RUN = False

RELEASE_STAGE = "testing"
