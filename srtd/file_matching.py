from typing import List
from schema import FileObject
from weaviate_client import WeaviateClient

class FileMatching:
    def __init__(self):
        self.weaviate_client = WeaviateClient()

    def match_files(self, input_str: str, file_list: List[FileObject]) -> List[FileObject]:
        """Match files based on the input string and return matching files"""
        pass
