from typing import List
from schema import FileObject
from file_matching import FileMatching

class SemanticFileMatching(FileMatching):
    def match_files(self, input_str: str, file_list: List[FileObject]) -> List[FileObject]:
        """Match files using semantic search"""
        results = self.weaviate_client.semantic_search(input_str, limit=10)
        return [file for file, _ in results]