from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="category name")
    
    model_config = ConfigDict(from_attributes=True)

class CategoryResponse(CategoryBase):
    id: int
