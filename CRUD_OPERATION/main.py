from sqlalchemy.orm import Session
from sql_app import schemas, databases
from utils import *
from fastapi import FastAPI
app = FastAPI()


@app.post('/adicionar_produtos', response_model=schemas.criar_prod)
def adição_produtos(
produto: schemas.criar_prod,
db: Session = databases.Depends(databases.get_db)):
    return adicionar_produtos(produto, db)

@app.get ('/verificar/{id}', response_model = schemas.get_prod) 
def consultas_de_produto(
    id: int, 
    db: Session = Depends(databases.get_db)):
    return consultar_produto(id, db)

@app.delete ('/deletar_produto/{id}',response_model = schemas.remove_prod)
def remoção_dos_produto(
    id: int, 
    db:Session=Depends(databases.get_db)):
    return remover_produto(id, db)

@app.put('/atualizar_produto/{id}', response_model=schemas.AtualizacaoResponse)
def atualização_produto(id: int, produto_update: schemas.ProdutoUpdate, db: Session = Depends(databases.get_db)):
    return atualizar_produto(id, produto_update, db)

#Obs : Sempre passar db como terceiro parametro