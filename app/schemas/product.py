from pydantic import BaseModel, Field

class ProductRequest(BaseModel):
    name: str = Field(max_length=150)
    description: str = Field(max_length=255)
    price: float = Field(gt=0)
    stock: int = Field(gt=0)