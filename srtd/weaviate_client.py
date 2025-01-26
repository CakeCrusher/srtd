# src/services/weaviate_client.py

from typing import List, cast
import weaviate
from weaviate.classes.config import Configure
from weaviate.classes.query import MetadataQuery
import os


class WeaviateClient:
    def __init__(self):
        headers = {
            "X-VoyageAI-Api-Key": os.getenv("VOYAGEAI_API_KEY", ""),
        }
        if not headers["X-VoyageAI-Api-Key"]:
            raise ValueError("Please provide a VoyageAI API key")
        self.client = weaviate.connect_to_local(
            host=os.getenv("WEAVIATE_HOST", "localhost"),
            port=int(os.getenv("WEAVIATE_PORT", "8080")),
            grpc_port=int(os.getenv("WEAVIATE_GRPC_PORT", "50051")),
            headers=headers,
        )
        meta_info = self.client.get_meta()
        print(meta_info)

    def ensure_collection(self, collection_name: str) -> bool:
        if self.client.collections.exists(collection_name):
            print(f"Collection '{collection_name}' already exists")
            return True
        else:
            self.client.collections.create(
                collection_name,
                vectorizer_config=[
                    Configure.NamedVectors.text2vec_voyageai(
                        name="title_vector",
                        source_properties=["text_to_embed"],
                        model="voyage-2",
                    )
                ],
            )
            print(f"Collection '{collection_name}' created successfully")
            return True

    # def add_objects(self, collection_name: str, objects_data: List[ChunkData]) -> None:
    #     if not self.client.collections.exists(collection_name):
    #         raise ValueError(f"Collection '{collection_name}' does not exist")
    #     collection = self.client.collections.get(collection_name)
    #     with collection.batch.dynamic() as batch:
    #         for obj_data in objects_data:
    #             batch.add_object(obj_data.model_dump())
    #     if len(collection.batch.failed_objects) > 0:
    #         print(f"Failed to import {len(collection.batch.failed_objects)} objects")
    #         for failed in collection.batch.failed_objects:
    #             print(f"Failed to import object with error: {failed.message}")
    #     print(
    #         f"Added {len(objects_data) - len(collection.batch.failed_objects)} objects to collection '{collection_name}'"
    #     )

    # def retrieve_objects(
    #     self, collection_name: str, query: str, limit: int = 10
    # ) -> List[ChunkData]:
    #     self.ensure_collection(collection_name)
    #     collection = self.client.collections.get(collection_name)

    #     # Check if the collection is empty
    #     object_count = collection.aggregate.over_all(total_count=True).total_count
    #     if object_count == 0:
    #         print(f"The collection '{collection_name}' is empty.")
    #         return []

    #     response = collection.query.hybrid(
    #         query=query,
    #         limit=limit,
    #         include_vector=False,
    #     )
    #     weaviate_objects = [obj.properties for obj in response.objects]

    #     chunk_objects = cast(List[dict], weaviate_objects)
    #     for chunk in chunk_objects:
    #         if chunk is None:
    #             continue
    #         else:
    #             chunk["metadata"]["original_uuid"] = str(
    #                 chunk["metadata"]["original_uuid"]
    #             )
    #             chunk["metadata"]["doc_id"] = str(chunk["metadata"]["doc_id"])
    #     chunk_objects = [ChunkData(**cast(dict, obj)) for obj in weaviate_objects]

    #     return chunk_objects

    def delete_collection(self, collection_name: str) -> None:
        if not self.client.collections.exists(collection_name):
            raise ValueError(f"Collection '{collection_name}' does not exist")
        self.client.collections.delete(collection_name)
        print(f"Collection '{collection_name}' deleted successfully")