#!/usr/bin/env python3

from dotenv import load_dotenv
from semantic_file_matching import SemanticFileMatching
from semantic_file_uploading import SemanticFileUploading
from schema import FileObject

load_dotenv()

semantic_file_matching = SemanticFileMatching()
file1 = FileObject(
    name="init.py",
    path=r"C:\Projects\srtd\srtd\__init__.py",
    ai_summary="This is a test file",
    created_at=1716854400,
    is_directory=False,
    string_content_truncated="This is a test file",
)
file2 = FileObject(
    name="test2.txt",
    path=r"C:\Users\jason\Desktop\test2.txt",
    ai_summary="This is a test file",
    created_at=1716854400,
    is_directory=False,
    string_content_truncated="This is a test file",
)
uploading = SemanticFileUploading()
uploading.upload_files([file1, file2])
# results = semantic_file_matching.match_files("computer", [file1, file2])
# for result in results:
#     print(result.ai_summary)
    
