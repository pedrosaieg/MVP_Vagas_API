from pydantic import BaseModel
from typing import Optional, List
from models.empresa import Empresa

from schemas import VagaSchema


class EmpresaSchema(BaseModel):
    """ Define como uma nova empresa a ser inserida deve ser representada
    """

    nome:str = "XPTO"
    ramo_atuacao:str = "Óleo e gás"
    sobre:str = "Empresa que atua no ramo de upstream"
    link:str = "www.xpto.com.br"
    tamanho:int = 200


class EmpresaViewSchema(BaseModel):
    """ Define como uma empresa será retornada.
    """
    id: int = 1
    nome:str = "XPTO"
    ramo_atuacao:str = "Óleo e gás"
    sobre:str = "Empresa que atua no ramo de upstream"
    link:str = "www.xpto.com.br"
    tamanho:int = 200
    vagas:List[VagaSchema]

class EmpresaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
    feita apenas com base no id da empresa.
    """
    id: int = 1

class EmpresaDelSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
    feita apenas com base no id da empresa.
    """
    message: str = "Removida com sucesso."
    id: int = 1

class EmpresaEditSchema(BaseModel):
    """ Define como uma empresa será editada.
    """
    id: int = 1
    nome:str = "XPTO"
    ramo_atuacao:str = "Óleo e gás"
    sobre:str = "Empresa que atua no ramo de upstream"
    link:str = "www.xpto.com.br"
    tamanho:int = 200

class ListagemEmpresasSchema(BaseModel):
    """ Define como a lista de empresas será retornada.
    """
    empresas:list[EmpresaSchema]

def apresenta_empresa(empresa: Empresa):
    """ Retorna uma representação da empresa seguindo o schema definido em
        EmpresaViewSchema.
    """
    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "ramo_atuacao": empresa.ramo_atuacao,
        "sobre": empresa.sobre,
        "link": empresa.link,
        "tamanho": empresa.tamanho,
        "vagas": [{"vaga": c.cargo} for c in empresa.vagas]
    }

def apresenta_empresas(empresas: List[Empresa]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for empresa in empresas:
        result.append({
            "id": empresa.id,
            "nome": empresa.nome,
            "ramo_atuacao": empresa.ramo_atuacao,
            "sobre": empresa.sobre,
            "link": empresa.link,
            "tamanho": empresa.tamanho,
            "vagas" : len(empresa.vagas)
        })

    return {"empresas": result}