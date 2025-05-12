from sqlalchemy import Column, String, Integer, Date, DateTime
from datetime import datetime, date
from typing import Union
from model import Base

class Aluno(Base):
    __tablename__ = 'aluno'

    id = Column("pk_aluno", Integer, primary_key=True)
    primeiro_nome = Column(String(50), nullable=False)
    segundo_nome = Column(String(50), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    data_insercao = Column(DateTime, default=datetime.now)

    def __init__(self, primeiro_nome: str, segundo_nome: str, cpf: str, data_nascimento: date,
                 data_insercao: Union[datetime, None] = None):
        """
        Cria um Aluno.

        Args:
            primeiro_nome: Primeiro nome do aluno.
            segundo_nome: Sobrenome do aluno.
            cpf: CPF do aluno (único).
            data_nascimento: Data de nascimento do aluno.
            data_insercao: Data de inserção na base de dados (default: agora).
        """
        self.primeiro_nome = primeiro_nome
        self.segundo_nome = segundo_nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.data_insercao = data_insercao if data_insercao else datetime.now()
