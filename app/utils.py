import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
DATABASE_URL = os.getenv("DATABASE_URL")

DATA_DIR = "data"