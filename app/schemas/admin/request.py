from pydantic import BaseModel,Field, ConfigDict

class AdminRoleUpdate(BaseModel):
    is_admin: bool

class AdminProductCreate(BaseModel):
    name: str
    stock: int = Field(ge = 0)
    price: float = Field(gt = 0)
    description: str | None = None
    product_type: str | None = None

class AdminProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = Field(default= None, gt = 0)
    stock: int | None = Field(default = None, ge = 0)
    description : str | None= None

class AdminStockUpdate(BaseModel):

    stock: int = Field(ge = 0)
    
