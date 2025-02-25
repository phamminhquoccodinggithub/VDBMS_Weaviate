# VDBMS_Weaviate

## Prerequisites

To run this example, you need:
- Docker (to run Weaviate)
- Python 3.8 or higher

## Setup instructions

1. Install the Python dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2. Run docker-compose to spin up an Weaviate instance and the CLIP inference container.
    ```bash
    docker compose up -d
    ```
3. Create the collection definition and import data, as well as some pre-prepared queries.
    ```bash
    python add_data.py
    ```
4. Start the Streamlit app.
    ```bash
    streamlit run app.py
    ```