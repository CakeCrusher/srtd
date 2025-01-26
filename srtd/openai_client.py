# src/services/openai_client.py

import os
from typing import Optional

from pydantic import BaseModel, Field

from pydantic import BaseModel, Field
from openai import OpenAI

from schema import FileObject
import os

class FileSummaryGenerator(BaseModel):
    """
    A summary of the file content.
    """
    summary: str = Field(..., description="The summary of the file content.")



class OpenAIClient:
    """
    A client for interacting with the OpenAI API.
    """

    def __init__(self):
        """
        Initializes the OpenAI client.

        Args:
            api_key (Optional[str]): The OpenAI API key. If not provided, it will be read from the OPENAI_API_KEY environment variable.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        print("API KEY", api_key)
        self.client = OpenAI(api_key=api_key)


    def file_summary(self, file: FileObject) -> str:
        """
        Summarizes the file content into a couple of sentences that convey the purpose of the file.

        Args:
            file (os.DirEntry): The file to summarize.

        Returns:
            str: The summary of the file.
        """
        # TODO: need to see how to get summmaries of files on chatgpt
        prompt = f"""
Summarizes the file content into a couple of sentences that convey the purpose of the file.

PATH
```{file.path}```

IS_DIRECTORY
```{file.is_directory}```

FILE CONTENT
```{file.string_content_truncated}```
        """.strip()

        try:
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "user", "content": prompt},
                ],
                response_format=FileSummaryGenerator,
            )

            summary_dict = completion.choices[0].message.parsed
            if not summary_dict:
                raise ValueError("Failed to generate a summary")
            return summary_dict.summary.strip()
        except Exception as e:
            raise ValueError(f"Failed to summarize file content: {str(e)}")
