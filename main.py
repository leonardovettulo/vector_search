from fastapi import FastAPI

from search.constants import (
    CHUNKS_JSON_PATH,
    DATA_FOLDER,
    TEXT_NUMBER_OF_TOP_RESULTS,
    VECTOR_NUMBER_OF_TOP_RESULTS,
)
from search.models import SearchRequest, SearchResponse, SearchResultItem
from search.search_text.text_search import ElasticTextSearch
from search.search_text.vector_search import VectorSearch
from search.vectorizer.parse_html import parse_html_files_to_chunks
from search.vectorizer.text_save import save_text_to_elasticsearch
from search.vectorizer.vectorize import create_embeddings_and_save

app = FastAPI()


@app.post("/search_vector", response_model=SearchResponse)
def search_vector(request: SearchRequest):
    vector_search = VectorSearch(collection="wikipedia")

    top_k = request.top_results or VECTOR_NUMBER_OF_TOP_RESULTS

    raw_results = vector_search.search(text=request.query, top_k=top_k)

    formatted_results = [
        SearchResultItem(
            doc_id=result[0]["doc_id"],
            title=result[0]["title"],
            subtitle=result[0]["subtitle"],
            content=result[0]["document"],
            score=result[1],
        )
        for result in raw_results
    ]

    return SearchResponse(results=formatted_results)


@app.post("/search_text", response_model=SearchResponse)
def search_text(request: SearchRequest):
    text_search = ElasticTextSearch(index_name="articles")

    top_k = request.top_results or TEXT_NUMBER_OF_TOP_RESULTS

    raw_results = text_search.search(text=request.query, top_k=top_k)

    formatted_results = [
        SearchResultItem(
            doc_id=result[0]["doc_id"],
            title=result[0]["title"],
            subtitle=result[0]["subtitle"],
            content=result[0]["content"],
            score=result[1],
        )
        for result in raw_results
    ]

    return SearchResponse(results=formatted_results)


@app.get("/vectorize_data")
def vectorize_data():

    number_of_documents = create_embeddings_and_save()

    return {"Number of documents": number_of_documents}


@app.get("/create_chunks")
def create_chunks():
    number_of_chunks = parse_html_files_to_chunks(
        folder_path=DATA_FOLDER, output_json_path=CHUNKS_JSON_PATH
    )

    return {"Number of chunks": number_of_chunks}


@app.get("/save_text_to_elastic")
def save_text_to_elastic():
    number_of_documents = save_text_to_elasticsearch()

    return {"Number of documents": number_of_documents}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
