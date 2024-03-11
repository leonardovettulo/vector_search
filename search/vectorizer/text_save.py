import json

from elasticsearch import Elasticsearch

from search.constants import CHUNKS_JSON_PATH, ELASTIC_PWD, ELASTIC_URL, ELASTIC_USR


def save_text_to_elasticsearch():
    es = Elasticsearch(
        [ELASTIC_URL],
        http_auth=(ELASTIC_USR, ELASTIC_PWD),
    )

    try:
        with open(CHUNKS_JSON_PATH, "r") as file:
            documents = json.load(file)
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON.")

    # Index name
    index_name = "articles"

    # Index each document in Elasticsearch
    for doc in documents:
        res = es.index(index=index_name, document=doc)
        print("Indexed Document ID:", res["_id"])

    return len(documents)
