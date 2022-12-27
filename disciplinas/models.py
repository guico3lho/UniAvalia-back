from sqlalchemy import Column, Integer, String

from database import Base


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    codigo = Column(String)
    carga_horaria = Column(Integer)

# drop a dataframe row if a column contains another string
