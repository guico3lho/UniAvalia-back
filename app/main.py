from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import models as models

import database as database

app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
#     "https://uniavalia.vercel.app/search"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/disciplinas')
def get_disciplinas(db: Session = Depends(get_db)):
    disciplinas = db.query(models.Disciplina).all()
    return disciplinas

@app.get('/disciplinas/{disciplina_id}')
def get_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    disciplina = db.query(models.Disciplina).filter(models.Disciplina.id == disciplina_id).first()
    return disciplina, disciplina.professores

@app.get('/professores')
def get_professores(db: Session = Depends(get_db    )):
    professores = db.query(models.Professor).all()
    return professores

@app.get('/professores/{professor_id}')
def get_professor(professor_id: int, db: Session = Depends(get_db)):
    professor = db.query(models.Professor).filter(models.Professor.id == professor_id).first()
    return professor, professor.disciplinas

@app.get('/disciplinas_professores')
def get_disciplinas_professores(db: Session = Depends(get_db)):
    disciplinas_professores = db.query(models.disciplina_professor).join(models.Disciplina).join(models.Professor).with_entities(
        models.disciplina_professor, models.Disciplina.nome.label('disciplina_nome'), models.Professor.nome.label('professor_nome')).all()
    return disciplinas_professores