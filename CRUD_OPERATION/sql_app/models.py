from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

#Isto irá criar uma tabela Itens, onde sera adicionado as informações dos produtos
Base = declarative_base()

class Item(Base):
    
    __tablename__ = "itens"

    id = Column(Integer, primary_key=True, index=True)
    produto = Column(String, index=True)
    quantidade = Column(Integer, index=True, nullable=False )
    valor = Column(Float, index=True)

