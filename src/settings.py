import os

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'local')
API_KEY = os.environ.get('API_KEY', None)
DOCS_URL = os.environ.get('DOCS_URL', None)
REDOC_URL = os.environ.get('REDOC_URL', None)

TRAINED_FILE_PATH = os.environ.get('TRAINED_FILE_PATH', './')
DEBUGGING_PORT = os.environ.get('DEBUGGING_PORT', 5051)
