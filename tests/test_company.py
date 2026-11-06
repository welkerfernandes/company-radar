import httpx
import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.infrastructure import PublicAPI

@pytest.fixture
def client(tmp_path):
    provider=PublicAPI(client=httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(500))))
    with TestClient(create_app(str(tmp_path/'test.db'),provider)) as client:
        client.headers['X-API-Key']='local-alpha'
        yield client
    provider.close()

def test_auth_and_openapi(client):
    assert client.get('/').status_code==200
    assert client.get('/openapi.json').status_code==200
    assert client.get('/health').json()=={'status':'ok'}
    client.headers['X-API-Key']='invalid'
    assert client.get('/api/history').status_code==401
    assert client.post('/api/analyze',json={'mode':'demo'}).status_code==401

def test_tenant_history_delete(client):
    response=client.post('/api/analyze',json={'mode':'demo'})
    assert response.status_code==200, response.text
    ident=response.json()['snapshot_id']
    assert len(client.get('/api/history').json())==1
    client.headers['X-API-Key']='local-beta'
    assert client.get('/api/history').json()==[]
    assert client.delete('/api/history/'+ident).status_code==404
    client.headers['X-API-Key']='local-alpha'
    assert client.delete('/api/history/'+ident).json()=={'deleted':True}
    assert client.get('/api/history').json()==[]

def test_provider_failure_no_fake_fallback(client):
    result=client.post('/api/analyze',json={'mode':'live'})
    assert result.status_code==502
    assert client.get('/api/history').json()==[]

def test_demo_registry_minimization(client):
    result=client.post('/api/analyze',json={'mode':'demo','cnpj':'00.000.000/0001-91'}).json()
    assert result['company']['cnpj']=='00000000000191'
    assert result['assessment']['status']=='consistent'
    assert result['provenance']['mode']=='demo'
    assert 'qsa' not in result['company'] and 'email' not in result['company']

@pytest.mark.parametrize('cnpj',['00000000000000','123','00000000000192','../../etc/passwd','abcdefghijklmn'])
def test_invalid_cnpj(client,cnpj):
    assert client.post('/api/analyze',json={'mode':'demo','cnpj':cnpj}).status_code==422

def test_inactive_and_missing_fields():
    from app.domain import assess
    result=assess({'situacao_cadastral':8})
    assert result['status']=='review'
    assert any(issue['code']=='not_active' for issue in result['issues'])

def test_live_identity_mismatch_is_rejected(tmp_path):
    api=PublicAPI(httpx.Client(transport=httpx.MockTransport(lambda r:httpx.Response(200,json={
           'cnpj':'11222333000181','situacao_cadastral':2}))))
    with TestClient(create_app(str(tmp_path/'live.db'),api)) as c:
        response=c.post('/api/analyze',json={'mode':'live'},headers={'X-API-Key':'local-alpha'})
    assert response.status_code==502
    api.close()
