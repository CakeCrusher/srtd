#!/usr/bin/env python3

from typing import List, Tuple
from thefuzz import process

from schema import FileObject
from semantic_file_matching import SemanticFileMatching

def getMatchesLexical(target: str, file_list: List[FileObject]) -> List[FileObject]:
    # Calculate fuzzy match scores for each file
    scored_files: List[Tuple[FileObject, int]] = []
    for file in file_list:
        score = process.extractOne(file.name, [target])[1]
        scored_files.append((file, score))
    
    # Sort by score
    sorted_files = sorted(scored_files, key=lambda x: x[1], reverse=False)

    print("Lexical matches:")
    for file in sorted_files:
        print(f"{file[0].name}\t{file[1]}")

    # Return just the files, discarding scores
    return [file for file, score in sorted_files]

def getMatchesSemantic(target: str, file_list: List[FileObject]) -> List[FileObject]:
    semantic_matcher = SemanticFileMatching()
    semantic_results = semantic_matcher.match_files(target, file_list)
    
    # print("\nSemantic matches:")
    # for file in semantic_results:
    #     print(f"{file.name}\t{file.ai_summary}")
    
    return semantic_results

def getMatches(target: str, file_list: List[FileObject]) -> List[FileObject]:
    # Get both types of matches
    lexical_results = getMatchesLexical(target, file_list)
    
    # For now, return only lexical results
    return lexical_results
