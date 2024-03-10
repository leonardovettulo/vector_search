from fastapi import FastAPI

from search.constants import DATA_FOLDER, VECTOR_NUMBER_OF_TOP_RESULTS
from search.models import SearchRequest, SearchResponse, SearchResultItem
from search.search_text.vector_search import VectorSearch
from search.vectorizer.parse_html import parse_html_files_to_chunks
from search.vectorizer.vectorize import create_embeddings_and_save

app = FastAPI()


@app.post("/search", response_model=SearchResponse)
def search_endpoint(request: SearchRequest):
    vector_search = VectorSearch(collection="wikipedia")

    top_k = request.top_results or VECTOR_NUMBER_OF_TOP_RESULTS

    raw_results = vector_search.search(text=request.query, top_k=top_k)

    formatted_results = [
        SearchResultItem(
            title=result[0]["title"],
            subtitle=result[0]["subtitle"],
            content=result[0]["document"],
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
    number_of_chunks = parse_html_files_to_chunks(folder_path=DATA_FOLDER)

    return {"Number of chunks": number_of_chunks}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
