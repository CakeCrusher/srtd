#!/usr/bin/env python3

from thefuzz import process

def getMatches(target: str, file_list):
    return sorted(file_list, key=lambda file: process.extractOne(file['name'], [target])[1], reverse=False)
