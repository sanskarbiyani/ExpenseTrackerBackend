from pydantic import BaseModel
from typing import Any, Dict, Optional

class APIResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    error: Optional[str] = None
 