from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sql_app import models
from fastapi import Depends

#Conexão com o banco de dados, verificar a documentação de fastapi
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@server:port/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Criar todas as colunas no banco de dados
models.Base.metadata.create_all(bind=engine)

#Serve para iniciar e fechar uma sessão para DB, util em caso de a função nao finalizar a sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy.orm import Session

session = Session()

try:
    # Código que realiza operações de banco de dados
    session.commit()  # Confirma a transação
except Exception as e:
    session.rollback()  # Reverte a transação em caso de erro
    raise
finally:
    session.close()  # Fecha a sessão