from search.constants import VECTOR_NUMBER_OF_TOP_RESULTS
from search.search_text.vector_search import VectorSearch
from search.vectorizer import vectorize


def search_text(text: str):

    vector_search = VectorSearch(collection="wikipedia")
    results = vector_search.search(text=text, top_k=VECTOR_NUMBER_OF_TOP_RESULTS)

    for result in results:
        print(f"{result[0]['title']} - {result[0]['subtitle']} - {result[1]}")


if __name__ == "__main__":

    vectorize.create_embeddings_and_save()

    SEARCH_QUERY = "bishop and knight checkmate"

    search_text(text=SEARCH_QUERY)
