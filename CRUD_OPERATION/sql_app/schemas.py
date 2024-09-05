from pydantic import BaseModel
from typing import Optional
#Aqui serão constadas as classes que serão utilizadas nas responses e requests

#  Parte request model
class criar_prod(BaseModel):
    produto : str
    quantidade: Optional[int] = 1
    valor : float

class get_prod (BaseModel):
      id: int
      produto: str
      quantidade: Optional[int] = 1
      valor: float

class remove_prod (BaseModel):
      message: str   

class update (BaseModel):
    produto: Optional[str] = None
    quantidade: Optional[int] = None
    valor: Optional[float] = None


#Fim da request model

#Parte response model
class message (BaseModel):
      message: str
     
#Classes de configurações das responses 
class Config:
        orm_mode = True  # Isso permite que o Pydantic converta automaticamente objetos do SQLAlchemy em JSON