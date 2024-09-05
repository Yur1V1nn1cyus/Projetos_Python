from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sql_app import schemas, databases, crud, models
import logging
app = FastAPI()

# Configuração para verificar os logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar todas as colunas no banco de dados
models.Base.metadata.create_all(bind=databases.engine)

#Serve para iniciar e fechar uma sessão para DB, util em caso de a função nao finalizar a sessão
def get_db():
    db = databases.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/adicionar_produtos', response_model=schemas.criar_prod)
def adicionar_produtos(
produto: schemas.criar_prod,
db: Session = Depends(get_db)):
    try:
        # Chame a função crud.create_item para inserir o produto no banco de dados
        item = crud.create_item(db, produto.produto, produto.quantidade, produto.valor)
        # Retorne a instância criada
        return item
    
    except Exception as e:
        # Logar erro
        logger.error(f"Erro ao adicionar o produto '{produto.produto}' ao banco de dados: {str(e)}")

@app.get ('/verificar/{id}', response_model = schemas.get_prod) 
def consultar_produto(
    id: int, 
    db: Session = Depends(get_db)):
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

@app.delete ('/deletar_produto/{id}',response_model = schemas.remove_prod)
def remover_produto(
    id: int, 
    db:Session=Depends(get_db)):
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

@app.put('/atualizar_produto/{id}', response_model=schemas.AtualizacaoResponse)
def atualizar_produto(id: int, produto_update: schemas.update, db: Session = Depends(get_db)):
    try:
        produto = db.query(models.Item).filter(models.Item.id == id).first()
        if produto:
            # Atualizar os campos conforme fornecido
            for key, value in produto_update.dict(exclude_unset=True).items():
                setattr(produto, key, value)
            db.commit()
            db.refresh(produto)
            produto_dict = {
                "id": produto.id,
                "produto": produto.produto,
                "quantidade": produto.quantidade,
                "valor": produto.valor
            }
            return schemas.AtualizacaoResponse( 
            produto=schemas.get_prod(**produto_dict),
            message = "Ação realizada com sucesso")

        else:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

    except Exception as e:
        # Mensagem de erro personalizada em caso de falha na atualização
        db.rollback()  # Reverte a transação em caso de erro
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Erro ao atualizar o produto no banco de dados.",
                "message": str(e)  # Inclui a mensagem de erro real
            }
        )
    return {"message": "Ação realizada com sucesso"}