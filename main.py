from fastapi import FastAPI

from search.constants import VECTOR_NUMBER_OF_TOP_RESULTS
from search.models import SearchRequest, SearchResponse, SearchResultItem
from search.search_text.vector_search import VectorSearch

app = FastAPI()


@app.post("/search", response_model=SearchResponse)
def search_endpoint(request: SearchRequest):
    vector_search = VectorSearch(collection="wikipedia")
    raw_results = vector_search.search(
        text=request.query, top_k=VECTOR_NUMBER_OF_TOP_RESULTS
    )

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
