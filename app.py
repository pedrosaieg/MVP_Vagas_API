from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from models import Session, Vaga
from logger import logger
from schemas import *
from flask_cors import CORS

from schemas.vaga import apresenta_vaga

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
vaga_tag = Tag(name="Vaga", description="Adição, visualização e remoção de vagas à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/vaga', tags=[vaga_tag],
          responses={"200": VagaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_vaga(form: VagaSchema):
    """Adiciona uma nova Vaga à base de dados

    Retorna uma representação das vagas e empresas associadas.
    """
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
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar vaga '{vaga.cargo}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar vaga '{vaga.cargo}', {error_msg}")
        return {"mesage": error_msg}, 400