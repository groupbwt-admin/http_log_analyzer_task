import os
from dotenv import load_dotenv


load_dotenv()
LOG_SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
LOG_SERVER_PORT = int(os.getenv("SERVER_PORT", "7649"))
ESTIMATOR = str(os.getenv("ESTIMATOR", "hyperloglog")).lower()
LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING")
