from fastapi import FastAPI, HTTPException, Depends, status
from sql_app import schemas, databases, crud, models
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import logging


#Função de consulta de produtos

def consultar_produto(
    id: int, 
    db: Session):
    produto = db.query(models.Item).filter(models.Item.id == id).first()
    
    if not produto :
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    produto_dict = produto.__dict__
    produto_dict.pop('_sa_instance_state', None)

    if produto_dict.get('quantidade') is None:
        produto_dict['quantidade'] = 1
            
    try:
            return schemas.get_prod(**produto_dict)
    except Exception as e:
            raise HTTPException(status_code=500, detail= "Erro ao validar")
    
# Configuração para verificar os logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    
#Função de adicionar produtos
def adicionar_produtos(
produto: schemas.criar_prod,
db: Session):
    try:
        # Chame a função crud.create_item para inserir o produto no banco de dados
        item = crud.create_item(db, produto.produto, produto.quantidade, produto.valor)
        # Retorne a instância criada
        return item
    
    except Exception as e:
        # Logar erro
        logger.error(f"Erro ao adicionar o produto '{produto.produto}' ao banco de dados: {str(e)}")

#Função de remover produtos
def remover_produto(
    id: int, 
    db:Session):
    #Buscar o produto no banco de dados
    produto = db.query(models.Item).filter(models.Item.id == id).first()
    #Condição caso produto não seja valido
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")    
    
    #Remover produto do db
    db.delete(produto)
    #Confirmar remoção
    db.commit()

    return {"message": "Ação realizada com sucesso"}

def atualizar_produto(id: int, produto_update: schemas.ProdutoUpdate, db: Session):
    try:
        # Busca o produto no banco de dados
        produto = db.query(models.Item).filter(models.Item.id == id).first()
        
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        # Atualiza os campos fornecidos
        for key, value in produto_update.dict(exclude_unset=True).items():
            setattr(produto, key, value)

        # Commit das mudanças no banco de dados
        db.commit()
        db.refresh(produto)

        # Monta o dicionário com os dados atualizados
        produto_dict = {
            "id": produto.id,
            "produto": produto.produto,
            "quantidade": produto.quantidade,
            "valor": produto.valor
        }

        # Retorna a resposta de sucesso com o produto atualizado
        return schemas.AtualizacaoResponse(
            produto=schemas.get_prod(**produto_dict),
            message="Ação realizada com sucesso"
        )

    except Exception as e:
        print(f"Erro ocorrido: {e}")  # Adicionar um log simples para verificar o erro
        print(f"Rollback no objeto: {db}")  # Verifica se `db` está correto
        db.rollback()  # Certifique-se de que o rollback é feito na sessão correta
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar o produto: {str(e)}"
        )