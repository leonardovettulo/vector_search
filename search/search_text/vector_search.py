from typing import Any

from qdrant_client import QdrantClient

from search.constants import EMBEDDINGS_MODEL, QDRANT_URL


class VectorSearch:
    """Implements vector search functionality using the Qdrant vector database."""

    def __init__(self, collection: str) -> None:
        """
        Initializes the VectorSearch with the given collection name.

        :param collection: The name of the collection to search within.
        """
        self.collection: str = collection
        self.qdrant_client: QdrantClient = QdrantClient(QDRANT_URL)
        self.qdrant_client.set_model(EMBEDDINGS_MODEL)

    def search(self, text: str, top_k: int) -> list[tuple[Any, float]]:
        """
        Performs a search query in the specified collection using the given text.

        :param text: The query text to search for.
        :param top_k: The number of top results to return.
        :return: A list of tuples containing metadata and score of each hit.
        """
        try:
            search_result = self.qdrant_client.query(
                collection_name=self.collection,
                query_text=text,
                query_filter=None,  # No filters for now
                limit=top_k,  # Get the top k results
            )
        except Exception as e:
            print(f"An error occurred during search: {e}")
            return []

        metadata = [(hit.metadata, hit.score) for hit in search_result]
        return metadata
