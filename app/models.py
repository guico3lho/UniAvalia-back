from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


disciplina_professor = Table('disciplina_professor', Base.metadata,
                             Column('disciplina_id', Integer, ForeignKey('disciplina.id')),
                             Column('professor_id', Integer, ForeignKey('professor.id')))



class Disciplina(Base):
    __tablename__ = "disciplina"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    codigo = Column(String)
    professores = relationship("Professor", secondary=disciplina_professor, back_populates="disciplinas")


class Professor(Base):
    __tablename__ = "professor"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    disciplinas = relationship("Disciplina", secondary=disciplina_professor, back_populates="professores")

# class Professor_Disciplina(Base):
#     __tablename__ = "professores_disciplinas"
#     id = Column(Integer, primary_key=True, index=True)
#     professor_id = Column(Integer, ForeignKey('professores.id'))
#     disciplina_id = Column(Integer, ForeignKey('disciplinas.id'))
    # disciplinas = relationship("Disciplina", secondary=disciplina_professor, back_populates="professores")

# drop a dataframe row if a column contains another string

# class DisciplinaProfessorDetails(Base):
#     __tablename__ = 'disciplina_professor_details'
#     disciplina = Column(String, primary_key=True)
#     professor = Column(String, primary_key=True)
