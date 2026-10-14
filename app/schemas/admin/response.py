from pydantic import BaseModel,ConfigDict


class AdminUserResponse(BaseModel):
    id: int
    user_name: str
    email: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)
    ##Confid_dict = Pydantic ko SQLAlchemy Product object ke attributes se response banane deta hai.

class ProductPhotoResponse(BaseModel):
    id: int
    url: str

    model_config = ConfigDict(from_attributes=True)


class AdminProductCreateReasponse(BaseModel):
    id: int
    name: str
    price: float 
    stock : int | None
    description: str | None
    product_type: str | None
    user_id: int | None
    photos: list[ProductPhotoResponse] = []

    model_config = ConfigDict(from_attributes=True)
    