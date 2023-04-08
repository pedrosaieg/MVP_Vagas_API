from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from models import Session, Vaga, Empresa
from logger import logger
from schemas import *
from flask_cors import CORS

from sqlalchemy.exc import IntegrityError

from schemas.vaga import apresenta_vaga, apresenta_vagas

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
    
@app.get('/vaga', tags=[vaga_tag],
        responses={"200": VagaViewSchema, "404": ErrorSchema})
def get_vaga(query: VagaBuscaSchema):
    """Faz a busca por uma vaga com base no id
    
    Retorna uma representação da vaga.
    """
    vaga_id = query.id
    logger.debug(f"Coletando dados sobre a empresa #{vaga_id}")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    vaga = session.query(Vaga).filter(Vaga.id == vaga_id).first()

    if not vaga:
        error_msg = "Vaga não encontrada na base."
        return {"message": error_msg}, 404
    else:
        logger.debug(f'%Vaga {vaga_id} encontrada')
        return apresenta_vaga(vaga), 200
    
@app.get('/vagas', tags=[vaga_tag],
        responses={"200": ListagemVagasSchema, "404": ErrorSchema})
def get_vagas():
    """Faz a busca por todas as vagas cadastradas
    
    Retorna uma representação da listagem de vagas.
    """
    logger.debug(f"Coletando vagas.")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    vagas = session.query(Vaga).all()

    if not vagas:
        return {"vagas": []}, 200
    else:
        logger.debug(f'%d vagas encontradas' % len(vagas))
        return apresenta_vagas(vagas), 200
   
@app.delete('/vaga', tags=[vaga_tag],
            responses={"200": VagaDelSchema, "404": ErrorSchema})
def del_vaga(query: VagaBuscaSchema):
    """Deleta uma vaga a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    vaga_id = query.id
    logger.debug(f"Deletando dados sobre a vaga #{vaga_id}")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    vaga = session.query(Vaga).filter(Vaga.id == vaga_id).delete()
    session.commit()

    if not vaga:
        error_msg = "Vaga não encontrada na base."
        return {"message": error_msg}, 404
    else:
        logger.debug(f'%Vaga {vaga_id} removida.')
        return {"message": f"Vaga {vaga_id} removida."}, 200

