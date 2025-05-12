from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import date, datetime
from model.aluno import Aluno  # Modelo SQLAlchemy correspondente

class AlunoSchema(BaseModel):
    """ Define como um novo aluno deve ser representado """
    primeiro_nome: str
    segundo_nome: str
    cpf: str
    data_nascimento: date

    @validator("data_nascimento", pre=True)
    def parse_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Formato de data inválido. Use YYYY-MM-DD.")
        return v


class AlunoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura da busca de um aluno """
    cpf: str = "12345678900"


class AlunoViewSchema(BaseModel):
    """ Define como um aluno será retornado """
    id: int
    primeiro_nome: str
    segundo_nome: str
    cpf: str
    data_nascimento: date

    class Config:
        orm_mode = True  # permite usar from_orm com modelos SQLAlchemy


class ListagemDeAlunosSchema(BaseModel):
    """ Define como uma listagem de alunos será retornada """
    alunos: List[AlunoViewSchema]


def apresenta_aluno(aluno: Aluno):
    """ Retorna uma representação do aluno """
    return {
        "id": aluno.id,
        "primeiro_nome": aluno.primeiro_nome,
        "segundo_nome": aluno.segundo_nome,
        "cpf": aluno.cpf,
        "data_nascimento": aluno.data_nascimento
    }


def apresenta_aluno_lista(alunos: List[Aluno]):
    """ Retorna uma representação da lista de alunos """
    return {
        "alunos": [apresenta_aluno(aluno) for aluno in alunos]
    }


class AlunoDelSchema(BaseModel):
    """ Define a estrutura do dado retornado após a remoção de um aluno """
    message: str
    cpf: str
