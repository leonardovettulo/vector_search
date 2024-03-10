from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_results: int | None = None


class SearchResultItem(BaseModel):
    title: str
    subtitle: str
    content: str
    score: float


class SearchResponse(BaseModel):
    results: list[SearchResultItem]
