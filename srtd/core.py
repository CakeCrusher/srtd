#!/usr/bin/env python3

import os

def buildFileTree(source_dir):
    print(f"Source dir is {source_dir}")
    if not os.path.exists(source_dir):
        print(f"Path \"{source_dir}\" doesn't exist")
        return
    if not os.path.isdir(source_dir):
        print(f"Path \"{source_dir}\" is not a directory")
    else:
        print("cool path bro")
