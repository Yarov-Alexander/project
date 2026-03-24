from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewCreate(BaseModel):
    product_id: int
    comment: Optional[str] = None
    grade: int = Field(..., ge=1, le=5)


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    comment: Optional[str]
    comment_date: datetime
    grade: int
    is_active: bool

    class Config:
        from_attributes = True