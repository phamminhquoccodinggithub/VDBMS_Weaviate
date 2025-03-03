import weaviate
import weaviate.classes as wvc
from weaviate.util import generate_uuid5
from weaviate import WeaviateClient
from weaviate.collections.classes.batch import BatchObjectReturn
import base64
from pathlib import Path

import json

with open('text.json', 'r') as file:
    query_data = json.load(file)
    query_data = query_data['vn']

with open('data/description.json', 'r', encoding='utf-8') as f:
    # Load JSON data
    data = json.load(f)

COLLECTION_NAME = "MultiModalCollection"
imgdir = Path("data/image")


def connect() -> WeaviateClient:
    return weaviate.connect_to_local()


def delete_existing(client: WeaviateClient) -> bool:
    client.collections.delete(COLLECTION_NAME)
    return True


def define_collection(client: WeaviateClient) -> bool:
    client.collections.create(
        name=COLLECTION_NAME,
        vectorizer_config=wvc.config.Configure.Vectorizer.multi2vec_clip(
            image_fields=["image"],
            vectorize_collection_name=False,
        ),
        generative_config=wvc.config.Configure.Generative.openai(),
        properties=[
            wvc.Property(
                name="image",
                data_type=wvc.config.DataType.BLOB,
            ),
            wvc.Property(
                name="filename",
                data_type=wvc.config.DataType.TEXT,
                # skip_vectorization=True,  # Not vectorizing for demonstrative purposes
            ),
            wvc.Property(
                name="description",
                data_type=wvc.config.DataType.TEXT,
            ),
            wvc.Property(
                name="conclusion",
                data_type=wvc.config.DataType.TEXT,
            ),
        ],
    )
    return True


def import_data(client: WeaviateClient) -> BatchObjectReturn:
    mm_coll = client.collections.get(COLLECTION_NAME)

    data_objs = list()
    for f in imgdir.glob("*.jpg"):
        b64img = base64.b64encode(f.read_bytes()).decode()

        data_props = {
            "image": b64img,
            "filename": f.name,
            "description": None,
            "conclusion": None
        }

        for patient in data:
            if patient["ID"] == "-".join(f.name.split('-')[:2]):
                data_props["description"] = patient["Mô tả"]
                data_props["conclusion"] = patient["Kết luận"]

        data_obj = wvc.data.DataObject(
            properties=data_props, uuid=generate_uuid5(f.name)
        )
        data_objs.append(data_obj)

    insert_response = mm_coll.data.insert_many(data_objs)

    print(f"{len(insert_response.all_responses)} insertions complete.")
    print(f"{len(insert_response.errors)} errors within.")
    if insert_response.has_errors:
        for e in insert_response.errors:
            print(e)

    return insert_response


def demo_query(client: WeaviateClient):
    mm_coll = client.collections.get(COLLECTION_NAME)

    response = mm_coll.aggregate.over_all(total_count=True)
    print(f"Object count: {response.total_count}")

    for q in query_data:
        response = mm_coll.query.near_text(q, limit=3)
        print(f"\n{'*'*10} \t Query: \t {'*'*10}\n")
        print(f"\t\t {q} \n")
        print(f"{'*'*10} \t RESULTS: \t {'*'*10}\n")
        for r in response.objects:
            print(r.uuid)
            print(r.properties["filename"])
            print(r.properties['description'])
            print(r.properties['conclusion'])
    return True


def update_data(client: WeaviateClient, uuid, update_props: dict):
    """
    Updates data in the collection based on filename or UUID.

    Args:
        client: Weaviate client.
        uuid: UUID to identify the object.
        update_props: Dictionary containing properties to update.
    """
    mm_coll = client.collections.get(COLLECTION_NAME)
    
    mm_coll.data.update(uuid=uuid, properties=update_props)


def delete_data(client: WeaviateClient, uuid):
    """
    Delete data in the collection based on  UUID.

    Args:
        uuid.
    """
    mm_coll = client.collections.get(COLLECTION_NAME)
    
    mm_coll.data.delete_by_id(uuid=uuid)


def main():
    client = connect()
    delete_existing(client)
    define_collection(client)
    import_data(client)
    # demo_query(client)

    # Example update by filename:
    # update_data(client, "7d5663f3-9295-508d-9171-761c20307c8a", {"description": "Updated Description", "conclusion":"Updated Conclusion"})
    # demo_query(client)
    # delete_data(client, "7d5663f3-9295-508d-9171-761c20307c8a")
    # demo_query(client)
    # Example update by UUID (you'd need to know the UUID):
    # example_uuid = "YOUR_UUID_HERE" # Replace with valid uuid
    # update_data(client, example_uuid, {"description": "Updated Description from UUID"}, by_filename=False)

if __name__ == "__main__":
    main()