# Welcome to the Xray Search Demo! 

## Dataset 
The dataset currently contains ten X-ray images.

## To run this demo, follow the order below:
1. Make sure you have Weaviate installed and set up. [Check out the documentation](https://weaviate.io/developers/weaviate/current/installation/index.html) for more information!:

Install docker: (https://docs.docker.com/engine/install/ubuntu/)

2. Run the docker file 
    ```bash
    docker compose up
    ```

### For the first time:
```bash
./run_all.sh
```

### Testing by:
```bash
python3 flask-app/application.py
```