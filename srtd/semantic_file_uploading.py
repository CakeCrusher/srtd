from typing import List
from schema import FileObject
from weaviate_client import WeaviateClient
import os
from pathlib import Path


class SemanticFileUploading:
    def __init__(self):
        """Initialize with a path and populate file_list"""
        self.file_list: List[FileObject] = []
        self.weaviate_client = WeaviateClient()


    # def __init__(self, path: str):
    #     """Initialize with a path and populate file_list"""
    #     self.file_list: List[FileObject] = []
    #     self.weaviate_client = WeaviateClient()
    #     self._populate_file_list(path)

    # def _populate_file_list(self, path: str) -> None:
    #     """Internal method to populate file_list from the given path"""
    #     path_obj = Path(path)
    #     if path_obj.is_file():
    #         self.file_list.append(self._create_file_object(path_obj))
    #     elif path_obj.is_dir():
    #         for file_path in path_obj.rglob('*'):
    #             if file_path.is_file():
    #                 self.file_list.append(self._create_file_object(file_path))

    # def _create_file_object(self, path: Path) -> FileObject:
    #     """Create a FileObject from a path"""
    #     return FileObject(
    #         name=path.name,
    #         path=str(path.absolute()),
    #         string_content_truncated=self._get_file_content(path),
    #         is_directory=False,
    #         created_at=int(path.stat().st_ctime),
    #         ai_summary=""  # This will be populated later
    #     )

    # def _get_file_content(self, path: Path) -> str:
    #     """Get the content of a file, with basic error handling"""
    #     try:
    #         return path.read_text(errors='ignore')
    #     except Exception as e:
    #         print(f"Error reading file {path}: {e}")
    #         return ""

    def upload_files(self, file_list: List[FileObject]) -> bool:
        """Upload all files in the given paths"""
        for file in file_list:
            self.weaviate_client.upsert_file(file)
        return True