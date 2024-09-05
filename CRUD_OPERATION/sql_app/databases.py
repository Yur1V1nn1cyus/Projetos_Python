from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Conexão com o banco de dados, verificar a documentação de fastapi
SQLALCHEMY_DATABASE_URL = "postgresql://yuri:teste123@localhost:8745/db_fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
