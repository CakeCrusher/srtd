# srtd/weaviate_client.py

from typing import List, cast
import weaviate
from weaviate.classes.config import Configure
from weaviate.classes.query import MetadataQuery, Filter
from weaviate.classes.config import Property, DataType
import os

from .schema import FileObject
from .openai_client import OpenAIClient
from dotenv import load_dotenv

from .schema import FileObject
from .openai_client import OpenAIClient
from .core import create_truncated_content
load_dotenv()

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
        try:
            if not os.getenv("COLLECTION_NAME"):
                raise ValueError("COLLECTION_NAME is not set")
            self.ensure_collection(os.getenv("COLLECTION_NAME"))
        except Exception as e:
            print(f"WeaviateClient INIT Error: {e}")
        self.collection = self.client.collections.get(os.getenv("COLLECTION_NAME"))

    def ensure_collection(self, collection_name: str) -> bool:
        if self.client.collections.exists(collection_name):
            print(f"Collection '{collection_name}' already exists")
            return True
        else:
            self.client.collections.create(
                collection_name,
                # properties=[
                #     Property(name="name", data_type=DataType.TEXT),
                #     Property(name="path", data_type=DataType.TEXT),
                #     Property(name="string_content_truncated", data_type=DataType.TEXT),
                #     Property(name="is_directory", data_type=DataType.BOOLEAN),
                #     Property(name="created_at", data_type=DataType.INT),
                #     Property(name="ai_summary", data_type=DataType.TEXT)
                # ],
                vectorizer_config=[
                    Configure.NamedVectors.text2vec_voyageai(
                        name="ai_summary_vector",
                        source_properties=["ai_summary"],
                        model="voyage-3-lite",
                    )
                ],
            )
            print(f"Collection '{collection_name}' created successfully")
            return True
        
    def upload_file(self, file: FileObject) -> bool:
        try:
            self.collection.data.insert(file.model_dump())
            return True
        except Exception as e:
            print(f"WeaviateClient upload_file Error: {e}")
            return False
        
    def upsert_file(self, file: FileObject) -> FileObject:
        # check if file exists if it does do nothing otherwise upload it
        response = self.collection.query.fetch_objects(
            limit=1,
            filters=Filter.by_property("path").equal(file.path)
        )
        if len(response.objects) > 0:
            print(f"{file.path}\t did not re-upload, it already exists")
            return FileObject(**response.objects[0].properties)
        else:
            print(f"{file.path}\t uploading...")
            openai_client = OpenAIClient()
            file.string_content_truncated = create_truncated_content(file.path)
            file.ai_summary = openai_client.file_summary(file)
            print(f"File summary: {file.ai_summary}")
            return self.upload_file(file)

    def semantic_search(self, query: str, limit: int = 10) -> List[tuple[FileObject, float]]:
        response = self.collection.query.hybrid(
            query=query,
            limit=limit,
            return_metadata=MetadataQuery(score=True)
        )
        return [(FileObject(**obj.properties), obj.metadata.score) for obj in response.objects]
    
    def retrieve_all_files_from_directory(self, directory: str) -> List[FileObject]:
        response = self.collection.query.fetch_objects()
        return [FileObject(**obj.properties) for obj in response.objects]
        
        
        

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