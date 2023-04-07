from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  models import Base

class Empresa(Base):
    __tablename__ = 'empresa'

    id = Column("pk_empresa", Integer, primary_key=True)
    nome = Column(String(100), unique=True)
    ramo_atuacao = Column(String(100))
    sobre = Column(String(100))
    link = Column(String(120), unique = True)
    tamanho = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now())
    vagas = relationship("Vaga", backref = "empresa")

    def __init__(self, nome:str, ramo_atuacao:str, sobre:str, link:str, tamanho:int,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Empresa

        Argumentos:
            nome: nome da empresa 
            ramo_atuacao: linha de atuação de mercado da empresa
            sobre: informações gerais da empresa
            link: página web da empresa
            tamanho: número médio de funcionários
            data_insercao: data de quando o produto foi inserido à base
        """
        self.id
        self.nome
        self.ramo_atuacao
        self.sobre
        self.link
        self.tamanho

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

 #   def adiciona_comentario(self, comentario:Comentario):
  #      """ Adiciona um novo comentário ao Produto
   #     """
    #    self.comentarios.append(comentario)

