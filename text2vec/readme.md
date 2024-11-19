

# Using on local, doccumentation:
    https://weaviate.io/developers/weaviate/quickstart/local

- Need to install Docker and Ollama first
    + https://docs.docker.com/get-started/get-docker/
    + https://ollama.com/download

- Then, download the nomic-embed-text and llama3.2 models by running the following command:
    ```bash
    ollama pull nomic-embed-text
    ollama pull llama3.2
    ```

- Start a Weaviate instance using Docker:
    ```bash
    docker compose up
    ```

### For the first time:
```bash
python3 quickstart_check_readiness.py
python3 quickstart_create_collection.py
python3 quickstart_import.py
```

### Testing by:
- Semantic search
```bash
python3 quickstart_neartext_query.py
```
- Retrieval augmented generation
```bash
python3 quickstart_rag.py
```