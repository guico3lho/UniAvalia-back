from fastapi import FastAPI, Depends
from pydantic import BaseModel
import os

from sqlalchemy.orm import Session

import schemas
import database
import models

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# migrate all tables
models.Base.metadata.create_all(bind=database.engine)


# migrate tables
# models.Base.metadata.create_all(bind=engine)

@app.post('/disciplinas')
def create_disciplina(request: schemas.Disciplina, db: Session = Depends(get_db)):
    new_disciplina = models.Disciplina\
        (nome=request.nome, codigo=request.codigo, carga_horaria=request.carga_horaria)
    db.add(new_disciplina)
    db.commit()
    db.refresh(new_disciplina)
    return new_disciplina

@app.get('/disciplinas')
def get_disciplinas(db: Session = Depends(get_db)):
    disciplinas = db.query(models.Disciplina).all()
    return disciplinas



# @app.post('/disciplinas')
# def create(request: models.Disciplina):
#     return print(os.getcwd())
