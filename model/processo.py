from sqlalchemy import Column, String, Integer, Date, DateTime
from datetime import datetime, date
from typing import Union
from model import Base

class Processo(Base):
    __tablename__ = 'processo'

    id = Column("pk_processo", Integer, primary_key=True)
    numero = Column(String(50), unique=True, nullable=False)
    descricao = Column(String(255), nullable=False)
    data_inicio = Column(Date, nullable=False) 
    data_fim = Column(Date, nullable=False)   
    data_insercao = Column(DateTime, default=datetime.now) 

    def __init__(self, numero: str, descricao: str, data_inicio: date, data_fim: date, 
                 data_insercao: Union[datetime, None] = None):
        """
        Cria um Processo.

        Args:
            numero: Número do processo (exemplo: '12345-67.2024.8.01.0001').
            descricao: Descrição sobre o processo.
            data_inicio: Data de início do processo (Obrigatório).
            data_fim: Data de conclusão do processo (Obrigatório).
            data_insercao: Data de inserção na base de dados (default: agora).
        """
        self.numero = numero
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.data_insercao = data_insercao if data_insercao else datetime.now()
