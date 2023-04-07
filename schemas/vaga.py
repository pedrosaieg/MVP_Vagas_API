from pydantic import BaseModel
from typing import Optional, List
from models.vaga import Vaga


class VagaSchema(BaseModel):
    """ Define como uma nova vaga a ser inserida deve ser representada
    """
    cargo:str = "Analista"
    modalidade_contrato:str = "PJ"
    modalidade_trabalho:str = "Presencial"
    empresa_id:int = 1
    descricao:str = "Planejar"
    responsabilidades:str = "Propor"
    conhecimentos:str = "Bom"


class VagaViewSchema(BaseModel):
    """ Define como uma vaga será retornada.
    """
    id: int = 1
    cargo: str = "Analista"
    modalidade_contrato:str = "CLT"
    modalidade_trabalho:str = "Presencial"
    empresa_id:int = 1
    descricao:str = "Planejar"
    responsabilidades:str = "Propor estratégias e alinhar/formalizar objetivos de performance junto aos clientes; Elaborar relatórios internos e externos de marketing digital"
    conhecimentos:str = "Bom raciocínio lógico; Perfil analítico e com foco em resultados; Habilidade de comunicação e relacionamento"

def apresenta_vaga(vaga: Vaga):
    """ Retorna uma representação da seguindo o schema definido em
        VagaViewSchema.
    """
    return {
        "id": vaga.id,
        "cargo": vaga.cargo,
        "modalidade_contrato": vaga.modalidade_contrato,
        "modalidade_trabalho": vaga.modalidade_trabalho,
        "empresa_id": vaga.empresa_id,
        "descricao": vaga.descricao,
        "responsabilidades": vaga.responsabilidades,
        "conhecimentos": vaga.conhecimentos
    }
