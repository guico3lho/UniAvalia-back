from pydantic import BaseModel


class Disciplina(BaseModel):
    nome: str
    codigo: str
    carga_horaria: int
