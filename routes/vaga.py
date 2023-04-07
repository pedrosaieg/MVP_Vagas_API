from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from models import Session, Vaga, Empresa
from logger import logger
from schemas import *
from flask_cors import CORS

from sqlalchemy.exc import IntegrityError

from schemas.vaga import apresenta_vaga

from app import app

vaga_tag = Tag(name="Vaga", description="Adição, visualização e remoção de vagas à base")

@app.post('/vaga', tags=[vaga_tag],
          responses={"200": VagaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_vaga(form: VagaSchema):
    """Adiciona uma nova Vaga à base de dados

    Retorna uma representação das vagas e empresas associadas.
    """
    empresa_id = form.empresa_id
    session = Session()
    empresa = session.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        # se empresa não encontrada
        error_msg = "Empresa não encontrada na base :/"
        logger.warning(f"Erro ao criar vaga à empresa'{empresa_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    vaga = Vaga(
       cargo = form.cargo,
       modalidade_contrato = form.modalidade_contrato,
       modalidade_trabalho = form.modalidade_trabalho,
       empresa_id = form.empresa_id,
       descricao = form.descricao,
       responsabilidades = form.responsabilidades,
       conhecimentos = form.conhecimentos)
    
    logger.debug(f"Adicionando vaga: '{vaga.cargo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(vaga)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionada vaga: '{vaga.cargo}'")
        return apresenta_vaga(vaga), 200

    except IntegrityError as e:
        error_msg = f"Ocorreu um erro de integridade ao tentar adicionar a vaga '{vaga.cargo}' à empresa '{empresa_id}' :/"
        logger.warning(f"Erro ao adicionar vaga '{vaga.cargo}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar vaga '{vaga.cargo}', {error_msg}")
        return {"mesage": error_msg}, 400