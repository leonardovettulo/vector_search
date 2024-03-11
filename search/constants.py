import os

QDRANT_URL = os.environ.get("QDRANT_URL", "http://qdrant_container:6333/")
ELASTIC_URL = os.environ.get("ELASTIC_URL", "http://elasticsearch_container:9200")
ELASTIC_USR = os.environ.get("ELASTIC_USR", "elastic")
ELASTIC_PWD = os.environ.get("ELASTIC_PWD", "elastic_password")
EMBEDDINGS_MODEL = os.environ.get(
    "EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
)
DATA_FOLDER = os.environ.get("DATA_FOLDER", "./data")
CHUNKS_JSON_PATH = os.environ.get("CHUNKS_JSON_PATH", "./data_chunks/chunks.json")
VECTOR_COLLECTION = os.environ.get("VECTOR_COLLECTION", "wikipedia")
VECTOR_NUMBER_OF_TOP_RESULTS = int(os.environ.get("VECTOR_NUMBER_OF_TOP_RESULTS", 5))
TEXT_NUMBER_OF_TOP_RESULTS = int(os.environ.get("TEXT_NUMBER_OF_TOP_RESULTS", 5))
