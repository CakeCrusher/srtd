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

    openai_client = OpenAIClient()
    print(openai_client.file_summary(FileObject(
        name="test.txt", 
        path=r"C:\Projects\srtd\srtd\__init__.py",  # Use raw string for Windows path
        string_content_truncated="...",
        is_directory=False, 
        created_at=0, 
        ai_summary="test"
    )))

    # core.buildFileTree(source_dir)

if __name__ == "__main__":
    main(sys.argv[1:])
