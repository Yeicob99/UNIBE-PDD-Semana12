from pydantic import BaseModel
from typing import List, Optional

class ArrayPayload(BaseModel):
    id: str
    data: List[float]
    op: str = "normalize"  # normalize|minmax|standardize
    use: Optional[str] = None  # "gpu"|"cpu" (no usado en esta versión)
