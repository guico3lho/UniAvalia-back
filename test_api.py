from fastapi import FastAPI

from typing import Optional

from pydantic import BaseModel

app = FastAPI()

class Disciplina(BaseModel):
    nome: str
    codigo: str
    carga_horaria: int



@app.get("/disciplinas")
def index(limit=10, sort: Optional[str] = None):

    if sort:
        return {'data': f'lista de {limit} disciplinas ordenadas por {sort}'}
    else:
        return {'data': f'lista de {limit} disciplinas'}

@app.get('/disciplinas/{id}')
def show(id: int):
    return {'data': id}

@app.post('/disciplinas')
def create(request: Disciplina):
   return {'data': f"disciplina {request.nome} criada"}

