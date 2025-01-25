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
    with os.scandir(os.path.abspath(source_dir)) as entries:
        for entry in entries:
            # skip symlinks because they break stuff
            if (entry.is_symlink()):
                continue

            file_info = {
                'path': entry.path,
                'name': entry.name,
                'is_dir': entry.is_dir(),

                # format of metadata field
                # https://docs.python.org/3/library/os.html#os.stat_result
                'metadata': entry.stat()
            }

            file_list.append(file_info)

    return file_list
