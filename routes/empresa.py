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
    """Adiciona uma nova empresa à base de dados

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
    
@app.get('/empresa', tags=[empresa_tag],
         responses={"200": EmpresaViewSchema, "404": ErrorSchema})
def get_empresa(query: EmpresaBuscaSchema):
    """Faz a busca por uma empresa a partir do id da empresa
    
    Retorna uma representação empresa.
    """
    empresa_id = query.id
    logger.debug(f"Coletando dados sobre a empresa #{empresa_id}")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    empresa = session.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        error_msg = "Empresa não encontrada na base."
        return {"message": error_msg}, 404
    else:
        logger.debug(f'%Empresa {empresa_id} encontrada')
        return apresenta_empresa(empresa), 200
    

@app.delete('/empresa', tags=[empresa_tag],
         responses={"200": EmpresaDelSchema, "404": ErrorSchema})
def delete_empresa(query: EmpresaBuscaSchema):
    """Deleta uma empresa a partir do id informado
    
    Retorna uma mensagem de confirmação da remoção.
    """
    empresa_id = query.id
    logger.debug(f"Deletando dados sobre a empresa #{empresa_id}")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    empresa = session.query(Empresa).filter(Empresa.id == empresa_id).delete()
    session.commit()

    if not empresa:
        error_msg = "Empresa não encontrada na base."
        return {"message": error_msg}, 404
    else:
        logger.debug(f'%Empresa {empresa_id} removida.')
        return {"message": f"Empresa {empresa_id} removida."}, 200
    

@app.put('/empresa', tags=[empresa_tag],
         responses={"200": EmpresaViewSchema, "404": ErrorSchema})
def edit_empresa(query: EmpresaEditSchema):
    """Edita uma empresa a partir do id informado
    
    Retorna uma mensagem de confirmação da remoção.
    """
    empresa_id = query.id

    logger.debug(f"Editando dados sobre a empresa #{empresa_id}")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    empresa = session.query(Empresa).filter(Empresa.id == empresa_id).update({"nome":query.nome, "ramo_atuacao": query.ramo_atuacao, "sobre": query.sobre, "link": query.link, "tamanho": query.tamanho})

    session.commit()

    if not empresa:
        error_msg = "Empresa não encontrada na base."
        return {"message": error_msg}, 404
    else:
        empresa_editada = session.query(Empresa).filter(Empresa.id == empresa_id).first()
        logger.debug(f'%Empresa {empresa_id} editada.')
        return apresenta_empresa(empresa_editada), 200