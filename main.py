from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

import models
import schemas
from crawler import parse_oferta

import database

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# migrate all tables




@app.get('/hello')
def get_hello():
    return {'message': 'Hello World'}
# migrate tables
# models.Base.metadata.create_all(bind=engine)
@app.post('/disciplinas')
def create_disciplina(request: schemas.Disciplina, db: Session = Depends(get_db)):
    new_disciplina = models.Disciplina \
        (nome=request.nome, codigo=request.codigo)
    db.add(new_disciplina)
    db.commit()
    db.refresh(new_disciplina)
    return new_disciplina

# @app.get("/disciplinas/")
# def get_disciplinas():
#     return parse_oferta(508, 2022,2)
@app.get('/disciplinas')
def get_disciplinas(db: Session = Depends(get_db)):
    disciplinas = db.query(models.Disciplina).all()
    return disciplinas


@app.get('/disciplinas/{disciplina_id}')
def get_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    disciplina = db.query(models.Disciplina).filter(models.Disciplina.id == disciplina_id).first()
    return disciplina

# @app.post('/disciplinas')
# def create(request: models.Disciplina):
#     return print(os.getcwd())
