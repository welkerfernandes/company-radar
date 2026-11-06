# Metodologia e avaliação

Motor de regras cadastrais, não machine learning. Situação diferente do código 2 e ausência de razão social, município, UF ou CNAE geram review. O estado consistent significa apenas que essas verificações passaram; não significa solvência, ausência de fraude ou conformidade jurídica.

## Evidência disponível

Testes cobrem invariantes, entradas inválidas, isolamento, falhas da fonte e modo demonstrativo.
Não existem benchmarks de produção, acurácia preditiva alegada ou métricas de clientes.
Fixtures sintéticas não servem como validação de generalização.

## Limites

Apenas CNPJ numérico de 14 dígitos: formatos alfanuméricos não são suportados. Dados de origem podem estar defasados. Não compara snapshots automaticamente, não faz consulta de sanções e não implementa análise de crédito. Respostas do provedor podem conter dados adicionais; contatos e sócios não são expostos nem persistidos no snapshot.
