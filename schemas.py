from typing import List

from pydantic import BaseModel


class Disciplina(BaseModel):
    nome: str
    codigo: str

class Professor(BaseModel):
    nome: str
