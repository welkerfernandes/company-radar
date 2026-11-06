"""CNPJ checksum and registry evidence. No credit scoring."""
import re

def normalize_cnpj(value):
    raw=re.sub(r'[.\-/\s]','',value)
    if not raw.isdigit() or len(raw)!=14 or len(set(raw))==1: raise ValueError('Invalid numeric CNPJ')
    for size,weights in [(12,[5,4,3,2,9,8,7,6,5,4,3,2]),(13,[6,5,4,3,2,9,8,7,6,5,4,3,2])]:
        remainder=sum(int(n)*w for n,w in zip(raw[:size],weights))%11
        check=0 if remainder<2 else 11-remainder
        if int(raw[size])!=check: raise ValueError('Invalid CNPJ check digits')
    return raw

def assess(company):
    issues=[]
    if company['situacao_cadastral']!=2: issues.append({'code':'not_active','detail':'Registry is not marked active'})
    for key in ('razao_social','municipio','uf','cnae_fiscal'):
        if not company.get(key): issues.append({'code':'missing_'+key,'detail':'Field absent in provider response'})
    return {'status':'review' if issues else 'consistent','issues':issues,
            'model':'registry-completeness-v1','notice':'Registry consistency is not a credit, fraud or compliance approval'}
