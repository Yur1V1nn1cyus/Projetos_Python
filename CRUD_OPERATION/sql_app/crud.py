from sqlalchemy.orm import Session
from .models import Item
#Isto vai criar uma tabela com o nome Itens
def create_item (db:Session, produto: str, quantidade: int, valor: float):
    if quantidade is None:
        raise ValueError("Quantidade deve ser um número inteiro válido")  

    db_item = Item(produto=produto, valor=valor, quantidade=quantidade)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

message = "Ação realizada com sucesso"