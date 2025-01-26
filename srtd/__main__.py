#!/usr/bin/env python3

import sys
from gui.__main__ import launch_gui
from dotenv import load_dotenv
from schema import FileObject
from weaviate_client import WeaviateClient
import os
# from openai_client import OpenAIClient


load_dotenv()

def main(args=None):
    #     source_dir = args[0]
    # else:
    #     print("Please provide a directory as a command line argument.")
    #     # return -1
    
    client = WeaviateClient()
    client.ensure_collection(os.getenv("COLLECTION_NAME"))

    launch_gui()

    # core.buildFileTree(source_dir)

if __name__ == "__main__":
    main(sys.argv[1:])
