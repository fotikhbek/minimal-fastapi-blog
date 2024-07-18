from pydantic import BaseModel
from typing import Optional
class PostScheme(BaseModel):
    header: str
    content: str
    author: str

class DeletedPostScheme(BaseModel):
    post_id: int
    result: str = 'Post {post_id} has been deleted'

class UpdatedPostScheme(BaseModel):
    id: int
    header: Optional[str]
    content: Optional[str]