#!/usr/bin/env python3

import os
from pathlib import Path
from typing import List
from schema import FileObject
import magic

def objectify(entry: os.DirEntry) -> FileObject:
        return FileObject(
            path= entry.path,
            name = entry.name,
            is_directory= entry.is_dir(),
            created_at= int(entry.stat().st_ctime),
            ai_summary="",
            string_content_truncated=create_truncated_content(entry.path)
        )

def create_truncated_content(file_path: str) -> str:
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()[:1000]
            truncated_content = "".join(lines)

        mime_type = magic.from_file(file_path, mime=True)

        if mime_type == "text/plain":
            summary = truncated_content
        else:
            summary = f"File of type {mime_type}"

        return summary

    except FileNotFoundError:
        return f"File {file_path} not found"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# collect top-level files in provided source_dir
def buildFileList(source_dir) -> List[FileObject]:
    # verify path passed in
    if not os.path.exists(source_dir):
        print(f"Path \"{source_dir}\" doesn't exist")
        return
    if not os.path.isdir(source_dir):
        print(f"Path \"{source_dir}\" is not a directory")
        return

    file_list = []

    # get directory object
    with os.scandir(os.path.abspath(source_dir)) as entries:
        for entry in entries:
            # skip symlinks because they break stuff
            if (entry.is_symlink()):
                continue

            file_list.append(objectify(entry))

    return file_list

# recursive helper for traversing filesystem
def destinationHelper(dir: str, curr_depth: int, max_depth:int = 10):
    dir_list = []

    print("dir to investigate: ", dir)
    if curr_depth > max_depth:
        return []
    # get directory object
    if os.path.isdir(dir):
        with os.scandir(os.path.abspath(dir)) as entries:
            for entry in entries:
                # skip symlinks and regular files
                if (entry.is_symlink() or not entry.is_dir()):
                    continue

                print(entry.name)
                # only append the path to the list because that's all that we care about
                dir_list.append(objectify(entry))

                # recurse in and apply children
                dir_list.extend(destinationHelper(entry.name, curr_depth+1))

    return dir_list


# recursively surface only directories to provide options for where to place files
def buildDestinationList(allowed_dests: list[str]) -> list[FileObject]:
    destination_list = [];

    for dest in allowed_dests:
        dest = os.path.expanduser(dest)
        print(f"allowed dest is {dest}")
        if os.path.isdir(dest):
            print("expanded")
            destination_list.extend(destinationHelper(dest, 0))

    return destination_list
