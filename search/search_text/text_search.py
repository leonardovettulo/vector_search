from typing import Any

from elasticsearch import Elasticsearch

from search.constants import ELASTIC_PWD, ELASTIC_URL, ELASTIC_USR
from search.models import SearchResultItem


class ElasticTextSearch:
    """Implements simple text search functionality using Elasticsearch."""

    def __init__(self, index_name: str) -> None:
        """
        Initializes the ElasticTextSearch with the given index name.

        :param index_name: The name of the index to search within.
        """
        self.index_name: str = index_name
        self.elasticsearch_client: Elasticsearch = Elasticsearch(
            [ELASTIC_URL],
            http_auth=(ELASTIC_USR, ELASTIC_PWD),
        )

    def search(self, text: str, top_k: int = 5) -> list[tuple[Any, float]]:
        """
        Performs a simple text search query in the specified index.

        :param query_text: The text to search for.
        :param top_k: The number of top results to return.
        :return: A list of tuples containing the document and score of each hit.
        """
        query = {
            "size": top_k,
            "query": {"match": {"content": text}},
        }

        try:
            search_result = self.elasticsearch_client.search(
                index=self.index_name, body=query
            )
            hits = search_result["hits"]["hits"]
        except Exception as e:
            print(f"An error occurred during search: {e}")
            return []

        return [(hit["_source"], hit["_score"]) for hit in hits]

    @staticmethod
    def format_result(raw_results: list[tuple]) -> list[SearchResultItem]:

        return [
            SearchResultItem(
                doc_id=result[0]["doc_id"],
                title=result[0]["title"],
                subtitle=result[0]["subtitle"],
                content=result[0]["content"],
                score=result[1],
            )
            for result in raw_results
        ]
