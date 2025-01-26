#!/usr/bin/env python3

import sys
import core
from dotenv import load_dotenv
from schema import FileObject
from weaviate_client import WeaviateClient
import os
from openai_client import OpenAIClient


load_dotenv()


def main(args=None):
    # if args and len(args) > 0:
    #     source_dir = args[0]
    # else:
    #     print("Please provide a directory as a command line argument.")
    #     # return -1
    
    # client = WeaviateClient()
    # client.ensure_collection(os.getenv("COLLECTION_NAME"))

    # openai_client = OpenAIClient()
    # print(openai_client.file_summary(FileObject(
    #     name="test.txt", 
    #     path=r"C:\Projects\srtd\srtd\__init__.py",  # Use raw string for Windows path
    #     string_content_truncated="...",
    #     is_directory=False, 
    #     created_at=0, 
    #     ai_summary="test"
    # )))

    client = WeaviateClient()
    results = client.retrieve_all_files_from_directory(r"C:\Projects\srtd\srtd")
    print("RESULTS:", results)
    for i, file in enumerate(results):
        print(f"{i}: {file.ai_summary}")
    # file1 = FileObject(
    #     name="test.txt", 
    #     path=r"C:\Projects\srtd\srtd\diff.py",  # Use raw string for Windows path
    #     string_content_truncated="...",
    #     is_directory=False, 
    #     created_at=0, 
    #     ai_summary="the stars are blue"
    # )
    # file2 = FileObject(
    #     name="test.txt", 
    #     path=r"C:\Projects\srtd\srtd\__init__.py",  # Use raw string for Windows path
    #     string_content_truncated="...",
    #     is_directory=False, 
    #     created_at=0, 
    #     ai_summary="why is my debugger not working"
    # )
    # upload_file1 = client.upsert_file(file1)
    # print(f"Uploaded file '{file1.path}': {upload_file1}")
    # upload_file2 = client.upsert_file(file2)
    # print(f"Uploaded file '{file2.path}': {upload_file2}")
    # upload_file3 = client.upsert_file(file2)
    # print(f"Uploaded file '{file2.path}': {upload_file3}")
    # results = client.semantic_search("computer")
    # print("RETRIEVED results:")
    # for file_obj, score in results:
    #     print(f"File: {file_obj.ai_summary}, Score: {score}")



    # core.buildFileTree(source_dir)

if __name__ == "__main__":
    main(sys.argv[1:])
