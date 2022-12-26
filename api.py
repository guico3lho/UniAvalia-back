from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.fields import List, Dict

from crawler import parse_oferta

from fastapi import Response

app = FastAPI()

class Disciplina(BaseModel):
    codigo: str
    nome: str

@app.get("/disciplinas/")
def get_disciplinas():
    return parse_oferta(508, 2022,2)


# @app.post("/disciplinas/")
# def create_disciplinas(disciplinas: List[Disciplina]):
#     return disciplinas
#
# @app.get("/disciplinas/")
# def read_disciplinas(disciplinas: List[Disciplina]):

# @app.post("/login")
# def login(user:User):
#     return {"msg": "login successful"}
