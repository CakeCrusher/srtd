#!/usr/bin/env python3

import sys
import core
from dotenv import load_dotenv
from weaviate_client import WeaviateClient
import os

load_dotenv()


def main(args=None):
    if args and len(args) > 0:
        source_dir = args[0]
    else:
        print("Please provide a directory as a command line argument.")
        # return -1
    
    client = WeaviateClient()
    client.ensure_collection(os.getenv("COLLECTION_NAME"))

    file_list = core.buildFileList(source_dir)

    if len(args) > 1 and args[1] == "print":
        print(file_list)

if __name__ == "__main__":
    main(sys.argv[1:])
