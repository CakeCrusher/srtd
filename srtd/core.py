#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
from typing import List, Optional
from .schema import FileObject
import PyPDF2

def objectify(entry: os.DirEntry) -> FileObject:
        return FileObject(
            path= entry.path,
            name = entry.name,
            is_directory= entry.is_dir(),
            created_at= int(entry.stat().st_ctime),
            ai_summary="",
            string_content_truncated=create_truncated_content(entry.path)
        )

def create_truncated_content(file_path: str, max_chars: int = 2000) -> str:
    """Get truncated content from a file, supporting text and PDF files"""
    if not os.path.exists(file_path):
        return "[File not found]"
        
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == '.pdf':
            return _read_pdf_content(file_path, max_chars)
        else:
            return _read_text_content(file_path, max_chars)
    except Exception as e:
        return f"[Error reading file: {str(e)}]"

def _read_text_content(file_path: str, max_chars: int) -> str:
    """Read content from text files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(max_chars)
            if len(content) == max_chars:
                content += "..."
            return content
    except UnicodeDecodeError:
        return "[Binary file]"

def _read_pdf_content(file_path: str, max_chars: int) -> str:
    """Read content from PDF files"""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = ""
            for page in reader.pages:
                content += page.extract_text()
                if len(content) >= max_chars:
                    return content[:max_chars] + "..."
            return content
    except Exception:
        return "[Error reading PDF]"

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
def move_files(selected_files: list[FileObject], destination: str) -> int:
    # Loop through the list of files and move each one
    for file in selected_files:
        # Construct the destination file path
        destination_path = os.path.normpath(os.path.join(destination, file.name))

        print(f"Trying to move {os.path.normpath(file.path)} to {destination_path}")
        try:
            # Attempt to move the file
            print(f"Success moved {os.path.normpath(file.path)} to {destination_path}")
            shutil.move(os.path.normpath(file.path), os.path.normpath(destination_path))

        except FileNotFoundError:
            print(f"The source file {file.path} does not exist.")
            return -1  # Return early on failure

        except PermissionError:
            print(f"Permission denied for moving {file.path}.")
            return -1  # Return early on failure

        except Exception as e:
            print(f"Failed to move {file.path}: {str(e)}")
            return -1  # Return early on failure

    # If all files are moved successfully, return 0
    return 0
