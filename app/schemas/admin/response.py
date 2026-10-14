from pydantic import BaseModel,ConfigDict


class AdminUserResponse(BaseModel):
    id: int
    user_name: str
    email: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)
    ##Confid_dict = Pydantic ko SQLAlchemy Product object ke attributes se response banane deta hai.

class AdminProductCreateReasponse(BaseModel):
    id: int
    name: str
    price: float 
    stock : int | None
    description: str | None
    user_id: int | None

    model_config = ConfigDict(from_attributes=True)
    