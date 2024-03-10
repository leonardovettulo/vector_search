
# Text Search Engine with Vector Database

### Introduction
In this project, we aim to create a sophisticated text search engine that leverages advanced vectorization techniques for efficient and accurate information retrieval. The core objective is to transform a collection of text documents into a searchable format by indexing it in a vector database (DB). This will enable high-speed and relevant search results for user queries by comparing the semantic similarity of the query against the indexed documents.

### Project Overview
The project involves several key steps:

- Data Preparation: We'll start with a dataset comprising 5-10 articles, which will be read from a file. This approach simplifies data handling and ensures that the system is scalable and can be tested with a controlled dataset.

- Text Chunking and Vectorization: The articles will be divided into manageable chunks. Each chunk will then be transformed into vector representations using open-source text embedding models. This process is crucial for capturing the semantic meaning of the text.

- Database Indexing: The generated vectors (embeddings) will be stored in an open-source graph database that supports vector search. This allows us to leverage the power of similarity search in high-dimensional space for retrieving the most relevant text chunks in response to a query.

- Query Processing: Users will input text queries, which are also vectorized using the same embedding model. The search engine will then find the top K most similar text chunks from the vector DB, effectively returning the most relevant results to the user.



## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Application with Docker](#running-the-application-with-docker)
  - [Building the Docker Image](#building-the-docker-image)
  - [Starting the Application with Docker Compose](#starting-the-application-with-docker-compose)
- [Development Setup](#development-setup)
  - [Setting Up a Conda Environment](#setting-up-a-conda-environment)
  - [Activating the Conda Environment](#activating-the-conda-environment)
- [Usage](#usage)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker and Docker Compose (for running the application in containers)
- Miniconda (for setting up the Conda environment)

### Installation

Explain how to clone your project repository. For example:

```bash
git clone git@github.com:leonardovettulo/vector_search.git
cd vector_search
```

## Running the Application with Docker

Follow these steps to run your application using Docker and Docker Compose.

### Building the Docker Image

You can build the Docker image by running:

```bash
docker-compose build
```

### Starting the Application with Docker Compose

To start the application with Docker Compose, run:

```bash
docker-compose up
```

This command starts all services defined in your `docker-compose.yml` file. These services include FastAPI and Qdrant Vector Database

## Development Setup

These instructions will help you set up a development environment using Conda.

### Setting Up a Conda Environment

To create a Conda environment for this project, run the following command in the project root directory:

```bash
conda create --name vector python=3.11
```

### Activating the Conda Environment

Activate the newly created Conda environment by running:

```bash
conda activate vector
```

After activating the environment, install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

Important! Run this to allow absolute imports

```bash
export PYTHONPATH=.
```
### Running tests

```bash
pytest tests/
```
## Usage

1. Place some html files in the data folder (for example page.html, page1.html, etc). Another option is to use the download_html.py script
2. Run the parse_html.py script to conver the html files to json chunks
3. Go to `http://localhost:8000/docs` to access the FastAPI console, use the `vectorize_data` endpoint to create the embeddings and save them into qdrant.
4. Use the `search` endpoint to search for text, you can optionally pick the number of results.
