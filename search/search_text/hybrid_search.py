import numpy as np

from search.constants import ELASTIC_INDEX, QDRANT_COLLECTION
from search.search_text.text_search import ElasticTextSearch
from search.search_text.vector_search import VectorSearch


def get_results(query: str, top_results: int):

    vector_search = VectorSearch(collection=QDRANT_COLLECTION)
    raw_vector_results = vector_search.search(text=query, top_k=top_results * 2)
    qdrant_results = vector_search.format_result(raw_results=raw_vector_results)
    qdrant_results_dict = [q.dict() for q in qdrant_results]

    text_search = ElasticTextSearch(index_name=ELASTIC_INDEX)
    raw_text_results = text_search.search(text=query, top_k=top_results * 2)
    elastic_results = text_search.format_result(raw_results=raw_text_results)
    elastic_results_dict = [e.dict() for e in elastic_results]

    return combine_results(
        qdrant_results=qdrant_results_dict, elastic_results=elastic_results_dict
    )[:top_results]


def z_score_normalize_scores(results: list[dict]) -> list[dict]:
    """Adjust the normalization function to use Z-score normalization"""
    scores = np.array([result["score"] for result in results])
    mean_score = np.mean(scores)
    std_score = np.std(scores)
    for result in results:
        if std_score > 0:
            result["normalized_score"] = (result["score"] - mean_score) / std_score
        else:
            result["normalized_score"] = 0  # If all scores are the same, normalize to 0
    return results


def get_document_details(doc_id: str, results: list[dict]) -> dict:
    for result in results:
        if result["doc_id"] == doc_id:
            return {
                "title": result.get("title"),
                "subtitle": result.get("subtitle"),
                "content": result.get("content"),
            }
    return {"title": "Unknown", "content": "No details available"}


def combine_results(
    qdrant_results: list[dict], elastic_results: list[dict]
) -> list[dict]:
    # Normalize scores
    qdrant_results_normalized = z_score_normalize_scores(qdrant_results)
    elastic_results_normalized = z_score_normalize_scores(elastic_results)

    # Combine and rerank
    combined_results: dict = {}
    weights = {"qdrant": 0.8, "elastic": 0.2}

    for result in qdrant_results_normalized:
        combined_results[result["doc_id"]] = (
            combined_results.get(result["doc_id"], 0)
            + result["normalized_score"] * weights["qdrant"]
        )

    for result in elastic_results_normalized:
        combined_results[result["doc_id"]] = (
            combined_results.get(result["doc_id"], 0)
            + result.get("normalized_score", 0) * weights["elastic"]
        )

    combined_results_list = [
        {"doc_id": doc_id, "score": score} for doc_id, score in combined_results.items()
    ]
    combined_results_sorted = sorted(
        combined_results_list, key=lambda x: x["score"], reverse=True
    )

    for item in combined_results_sorted:
        doc_id = item["doc_id"]
        details = get_document_details(doc_id, qdrant_results + elastic_results)
        item.update(details)

    return combined_results_sorted
