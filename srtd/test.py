#!/usr/bin/env python3

from dotenv import load_dotenv
from semantic_file_matching import SemanticFileMatching

load_dotenv()

semantic_file_matching = SemanticFileMatching()
results = semantic_file_matching.match_files("computer", [])
for result in results:
    print(result.ai_summary)
    
