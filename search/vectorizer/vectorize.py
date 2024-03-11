import json

from qdrant_client import QdrantClient, models
from tqdm import tqdm

from search.constants import (
    CHUNKS_JSON_PATH,
    EMBEDDINGS_MODEL,
    QDRANT_COLLECTION,
    QDRANT_URL,
)


def create_embeddings_and_save() -> int:
    """
    Creates embeddings for the text chunks and saves the vectos into a new collection.
    We are using fastembed in the background to speed up the process.
    """

    try:
        with open(CHUNKS_JSON_PATH, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON.")

    documents: list[str] = []  # For storing all the content that will be vectorized
    payload: list[dict] = []  # For storing the attributes that will be used as payload

    for chunk in data:
        if "content" in chunk:
            documents.append(chunk.pop("content"))
        payload.append(chunk)  # Store the rest of the attributes as a dict

    client = QdrantClient(
        url=QDRANT_URL,
        api_key=None,
    )

    client.set_model(EMBEDDINGS_MODEL)

    client.recreate_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=client.get_fastembed_vector_params(on_disk=True),
        # We use quantization to reduce the memory usage
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8, quantile=0.99, always_ram=True
            )
        ),
    )

    client.add(
        collection_name=QDRANT_COLLECTION,
        documents=documents,
        metadata=payload,
        ids=tqdm(range(len(payload))),
        parallel=0,
    )

    return len(documents)
