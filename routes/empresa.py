from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from models import Session, Empresa
from logger import logger
from schemas import *
from flask_cors import CORS

from sqlalchemy.exc import IntegrityError

from schemas.empresa import apresenta_empresa, apresenta_empresas

from app import app

empresa_tag = Tag(name="Empresa", description="Adição, visualização e remoção de empresas à base")

@app.post('/empresa', tags=[empresa_tag],
           responses={"200": EmpresaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_empresa(form: EmpresaSchema):
    """Adiciona uma nova Empresa à base de dados

    Retorna uma representação das empresas.
    """
    empresa = Empresa(
        nome = form.nome,
        ramo_atuacao= form.ramo_atuacao,
        sobre= form.sobre,
        link= form.link,
        tamanho= form.tamanho
    )

    logger.debug(f"Adicionando empresa: '{empresa.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(empresa)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionada empresa: '{empresa.nome}'")
        return apresenta_empresa(empresa), 200

    except IntegrityError as e:
        error_msg = f"Ocorreu um erro de integridade ao tentar adicionar a empresa '{empresa.nome}'"
        logger.warning(f"Erro ao adicionar empresa '{empresa.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar empresa '{empresa.nome}', {error_msg}")
        return {"mesage": error_msg}, 400

@app.get('/empresas', tags=[empresa_tag],
         responses={"200": ListagemEmpresasSchema, "404": ErrorSchema})
def get_empresas():
    """Faz a busca por todas as empresas cadastradas
    
    Retorna uma representação da listagem de empresas.
    """
    logger.debug(f"Coletando empresas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    empresas = session.query(Empresa).all()

    if not empresas:
        return {"empresas": []}, 200
    else:
        logger.debug(f'%d empresas encontradas' % len(empresas))
        return apresenta_empresas(empresas), 200