from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from models import Base, Empresa

class Vaga(Base):
    __tablename__ = 'vaga'

    id = Column("pk_vaga", Integer, primary_key=True)
    cargo = Column(String(140))
    modalidade_contrato = Column(String(30))
    modalidade_trabalho = Column(String(30))
    descricao = Column(String(1000))
    responsabilidades = Column(String(1000))
    conhecimentos = Column(String(1000))

    data_insercao = Column(DateTime, default=datetime.now())

    empresa_id = Column(Integer, ForeignKey("empresa.pk_empresa"), nullable=False)

    def __init__(self, cargo:str, modalidade_contrato:str, modalidade_trabalho:str, descricao:str, responsabilidades:str, conhecimentos:str, empresa_id:int,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Vaga

        Argumentos:
            cargo: nome do cargo
            modalidade_contrato: PJ ou CLT
            modalidade_trabalho: presencial, remoto ou híbrido
            empresa: nome da empresa
            descricao: descricao da vaga
            responsabilidades: responsabilidades que a pessoa contratada irá assumir
            conhecimentos: conhecimentos necessários/desejáveis para a vaga
            data_insercao: data de quando o produto foi inserido à base
        """
        self.cargo = cargo
        self.modalidade_contrato = modalidade_contrato
        self.modalidade_trabalho = modalidade_trabalho
        self.empresa_id = empresa_id
        self.descricao = descricao
        self.responsabilidades = responsabilidades
        self.conhecimentos = conhecimentos

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

 #   def adiciona_comentario(self, comentario:Comentario):
  #      """ Adiciona um novo comentário ao Produto
   #     """
    #    self.comentarios.append(comentario)

