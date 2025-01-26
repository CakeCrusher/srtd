#!/usr/bin/env python3

import os
import core
import filter

def main():
    # source_dir = input("Welcome to the sorted cli! Please enter a source folder to sort from: ")
    # print(f"Sorting in {source_dir}")

    source_dir = "~/Pictures"
    source_dir = os.path.expanduser(source_dir)
    print(f"Expanded: {source_dir}")

    file_list = core.buildFileList(source_dir)

    for file in file_list:
        print(file['name'])

    target = input("\nType string to match:\n> ")

    sorted = filter.getMatches(target, file_list)

    for file in sorted:
        print(file['name'])
