#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
from typing import List
from .schema import FileObject

def objectify(entry: os.DirEntry) -> FileObject:
        return FileObject(
            path= entry.path,
            name = entry.name,
            is_directory= entry.is_dir(),
            created_at= int(entry.stat().st_ctime),
            ai_summary="",
            string_content_truncated=""
        )

# collect top-level files in provided source_dir
def buildFileList(source_dir) -> List[FileObject]:
    source_dir = os.path.expanduser(source_dir)

    # verify path passed in
    if not os.path.exists(source_dir):
        print(f"Path \"{source_dir}\" doesn't exist")
        return []
    if not os.path.isdir(source_dir):
        print(f"Path \"{source_dir}\" is not a directory")
        return []

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

    if curr_depth > max_depth:
        return []
    # get directory object
    if os.path.isdir(dir):
        with os.scandir(os.path.abspath(dir)) as entries:
            for entry in entries:
                # skip symlinks and regular files
                if (entry.is_symlink() or not entry.is_dir()):
                    continue

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
        if os.path.isdir(dest):
            destination_list.extend(destinationHelper(dest, 0))

    return destination_list

# take a collection of file objects and move them to a destination
def move_files(selected_files: list[FileObject], destination: FileObject) -> int:

    # Loop through the list of files and move each one
    for file in selected_files:
        # Construct the destination file path
        destination_path = os.path.join(destination.path, file.name)
        # Move the file
        try:
            # shutil.move(file.path, destination_path)
            print(f"Moved {file.path} to {destination_path}")
            return 0
        except FileNotFoundError:
            print("The source file does not exist.")
        except PermissionError:
            print("Permission denied.")
        except Exception as e:
            print(f"Failed to move {file.path}: {str(e)}")

        # return -1 if failed
        return -1
