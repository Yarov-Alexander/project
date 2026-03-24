from pydantic import BaseModel, Field, ConfigDict


class CategoryCreate(BaseModel):
    name: str = Field(..., description="Название категории")
    parent_id: int | None = Field(None, description="ID родительской категории")
    model_config = ConfigDict(from_attributes=True)
class Category(BaseModel):
    id: int = Field(..., description="ID категории")
    name: str = Field(..., description="Название категории")
    parent_id: int | None = Field(default=None, description="ID родительской категории")
    is_active: bool = Field(..., description="Активность категории")

    model_config = ConfigDict(from_attributes=True)