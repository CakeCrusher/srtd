from typing import List
from schema import FileObject
from file_matching import FileMatching

class LexicalFileMatching(FileMatching):
    def match_files(self, input_str: str, file_list: List[FileObject]) -> List[FileObject]:
        """Match files using lexical/text-based search"""
        # TODO: Implement lexical matching logic
        pass 