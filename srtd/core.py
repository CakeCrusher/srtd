#!/usr/bin/env python3

import os
from pathlib import Path

# collect top-level files in provided source_dir
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
                'created_at': entry.stat().st_ctime
            }

            file_list.append(file_info)

    return file_list

# recursive helper for traversing filesystem
def destinationHelper(dir):
    dir_list = []

    # get directory object
    if os.path.isdir(dir):
        with os.scandir(os.path.abspath(dir)) as entries:
            for entry in entries:
                # skip symlinks and regular files
                if (entry.is_symlink() or not entry.is_dir()):
                    continue

                print(entry.name)
                # only append the path to the list because that's all that we care about
                dir_list.append(entry.path)

                # recurse in and apply children
                dir_list.extend(destinationHelper(entry))

    return dir_list


# recursively surface only directories to provide options for where to place files
def buildDestinationList(allowed_dests):
    destination_list = [];

    for dest in allowed_dests:
        if os.path.isdir(dest):
            destination_list.extend(destinationHelper(dest))

    return destination_list
