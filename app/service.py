from .native import invoke
from typing import Literal
from fastapi import HTTPException
from pydantic import BaseModel,Field,field_validator,ValidationError
from .domain import normalize_cnpj,assess
from .infrastructure import demo_metadata

class Command(BaseModel):
    mode: Literal['demo','live']='live'
    cnpj: str=Field(default='00000000000191',max_length=25)

    @field_validator('cnpj')
    @classmethod
    def valid_cnpj(cls,value): return normalize_cnpj(value)

class Registry(BaseModel):
    cnpj: str
    razao_social: str|None=None
    nome_fantasia: str|None=None
    situacao_cadastral: int=Field(strict=True)
    descricao_situacao_cadastral: str|None=None
    municipio: str|None=None
    uf: str|None=None
    cnae_fiscal: int|None=None
    cnae_fiscal_descricao: str|None=None
    data_inicio_atividade: str|None=None
    porte: str|None=None

def execute(command,api):
    if command.mode=='demo':
        data={'cnpj':command.cnpj,'razao_social':'EMPRESA DEMONSTRATIVA LTDA','nome_fantasia':'Fornecedor de exemplo',
              'situacao_cadastral':2,'descricao_situacao_cadastral':'ATIVA','municipio':'CALDAS NOVAS','uf':'GO',
              'cnae_fiscal':6201501,'cnae_fiscal_descricao':'Desenvolvimento de programas de computador sob encomenda',
              'data_inicio_atividade':'2020-01-01','porte':'MICRO EMPRESA'}
        metadata=demo_metadata(data)
    else:
        data,metadata=api.get('https://brasilapi.com.br/api/cnpj/v1/'+command.cnpj)
    try:
        company=Registry.model_validate(data).model_dump()
        if normalize_cnpj(company['cnpj'])!=command.cnpj: raise ValueError('Mismatched identity')
    except (ValidationError,ValueError,TypeError): raise HTTPException(502,'Company provider schema mismatch')
    # Publish only registry fields needed for this workflow; omit partners and contacts.
    payload='\n'.join([company['cnpj'],str(company['situacao_cadastral'])]+[str(bool(company.get(k))).lower() for k in ('razao_social','municipio','uf','cnae_fiscal')])+'\n'
    analysis=invoke(payload)
    if analysis is None: analysis={**assess(company),'engine':'python'}
    return {'company':company,'assessment':analysis,'provenance':metadata}
