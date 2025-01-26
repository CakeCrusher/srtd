from pydantic import BaseModel
# Attributes
# + name: str
# + path: str
# + string_content_truncated: str
# + is_directory: bool
# + created_at: str | int
# + ai_summary: str
class FileObject(BaseModel):
    """
    A file object.
    """
    name: str
    path: str
    string_content_truncated: str
    is_directory: bool
    created_at: str | int
    ai_summary: str

