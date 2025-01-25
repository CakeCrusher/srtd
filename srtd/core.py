#!/usr/bin/env python3

import os

def buildFileList(source_dir):
    print(f"Source dir is {source_dir}")

    # verify path passed in
    if not os.path.exists(source_dir):
        print(f"Path \"{source_dir}\" doesn't exist")
        return
    if not os.path.isdir(source_dir):
        print(f"Path \"{source_dir}\" is not a directory")
        return

    file_list = [];

    # get directory object
    with os.scandir(source_dir) as entries:
        for entry in entries:
            print(entry.name)
            # TODO: refine what goes into one of these objects
            file_info = {
                'path': entry.path,
                'name': entry.name,
                'is_file': entry.is_file(),
                'is_dir': entry.is_dir(),
            }
            file_list.append(file_info)
