#!/usr/bin/env python3

from typing import List
from thefuzz import process

from srtd.schema import FileObject

def getMatches(target: str, file_list: List[FileObject]) -> List[FileObject]:
    return sorted(file_list, key=lambda file: process.extractOne(file.name, [target])[1], reverse=False)
