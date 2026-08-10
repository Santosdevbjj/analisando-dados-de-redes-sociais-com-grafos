# 07 --- Reproducibility

## 1. Objetivo

Este documento define como reproduzir o projeto desde os datasets
originais até as consultas no Neo4j AuraDB.

Fluxo:

``` text
Download
  ↓
Preparação
  ↓
Validação
  ↓
Carga
  ↓
Validação do grafo
  ↓
Queries
  ↓
Evidências
```

## 2. Pré-requisitos

Obrigatórios:

-   Git;
-   Python 3.11+;
-   conta Neo4j;
-   Neo4j AuraDB Free;
-   Neo4j Browser/Workspace.

Recomendados:

-   VS Code;
-   GitHub;
-   ambiente virtual Python.

## 3. Clonar

``` bash
git clone https://github.com/Santosdevbjj/analisando-dados-de-redes-sociais-com-grafos.git
cd analisando-dados-de-redes-sociais-com-grafos
```

## 4. Ambiente Python

Linux/macOS:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Instalar dependências:

``` bash
pip install -r requirements.txt
```

## 5. Datasets

Obter no Kaggle:

``` text
Global Social Media Users by Age Gender 2025
Gen-Z Social Media Usage Dataset
```

Os datasets originais devem ser mantidos fora do GitHub quando forem
grandes.

## 6. Estrutura esperada

``` text
data/raw/
├── social_media_demographics.csv
└── genz_social_media_usage_1M.csv
```

Os nomes podem variar conforme a extração do ZIP; a origem deve ser
documentada.

## 7. Validação inicial

Confirmar:

``` text
arquivo existente
colunas esperadas
número de linhas
encoding
separador
```

Schema Gen-Z:

``` text
age
gender
country
daily_usage_hours
primary_platform
num_platforms_used
purpose
avg_session_minutes
night_usage
mental_health_score
addiction_level
screen_time_before_sleep
```

## 8. Preparação

Script:

``` text
scripts/prepare_datasets.py
```

Etapas:

1.  leitura;
2.  schema;
3.  tipos;
4.  nulos;
5.  domínios;
6.  ranges;
7.  normalização;
8.  ID técnico;
9.  amostras;
10. arquivos processados.

## 9. ID técnico

Criar:

``` text
genz_00000001
genz_00000002
...
```

Esse ID garante unicidade e auditoria, mas não representa identidade
real.

## 10. Amostragem

O dataset original possui:

``` text
1.000.000 registros
```

Para demonstração, utilizar uma amostra controlada, por exemplo:

``` text
10.000 observações
```

Documentar:

``` text
sample_size
sampling_method
source_rows
random_state
```

## 11. Amostragem determinística

``` python
sample = df.sample(
    n=10000,
    random_state=42
)
```

Com o mesmo dataset de entrada, a mesma seed produz a mesma amostra.

## 12. Amostras versionadas

Manter somente arquivos pequenos em:

``` text
data/samples/
```

Exemplo:

``` text
global_social_media_users_by_age_gender_2025_clean.csv
genz_social_media_usage_sample_1000.csv
genz_profile_aggregation_sample_500.csv
```

## 13. Neo4j AuraDB

Criar:

``` text
Neo4j AuraDB Free
```

Obter:

``` text
URI
username
password
```

Não publicar essas credenciais.

## 14. Variáveis de ambiente

Exemplo:

``` text
NEO4J_URI=neo4j+s://xxxxxxxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
```

O `.env` real deve permanecer fora do Git.

## 15. Ordem de execução

``` text
00_constraints.cypher
        ↓
01_load_global_demographics.cypher
        ↓
02_load_genz_profiles.cypher
        ↓
05_validation_queries.cypher
        ↓
03_business_queries.cypher
```

Quando aplicável:

``` text
04_graph_data_science.cypher
```

depois da validação.

## 16. Constraints

``` cypher
CREATE CONSTRAINT platform_name_unique IF NOT EXISTS
FOR (p:Platform)
REQUIRE p.name IS UNIQUE;
```

``` cypher
CREATE CONSTRAINT country_name_unique IF NOT EXISTS
FOR (c:Country)
REQUIRE c.name IS UNIQUE;
```

``` cypher
CREATE CONSTRAINT age_group_name_unique IF NOT EXISTS
FOR (a:AgeGroup)
REQUIRE a.name IS UNIQUE;
```

``` cypher
CREATE CONSTRAINT genz_profile_id_unique IF NOT EXISTS
FOR (u:GenZProfile)
REQUIRE u.profile_id IS UNIQUE;
```

## 17. Importação para AuraDB

Quando `LOAD CSV` for utilizado, o arquivo precisa estar disponível por
URL HTTP/HTTPS acessível pelo servidor Neo4j.

Exemplo:

``` cypher
LOAD CSV WITH HEADERS
FROM 'https://example.com/genz_profile.csv'
AS row
```

Caminhos locais como:

``` text
C:\Users\...
/mnt/data/...
```

não são acessíveis pelo servidor AuraDB.

Quando apropriado, utilizar também o Neo4j Data Importer.

## 18. Data Importer

Fluxo:

``` text
CSV
 ↓
Mapeamento de nodes
 ↓
Mapeamento de relationships
 ↓
Preview
 ↓
Import
```

Depois da carga, usar Cypher para validação e análise.

## 19. Validação pós-carga

Plataformas:

``` cypher
MATCH (p:Platform)
RETURN count(p) AS platforms;
```

Perfis:

``` cypher
MATCH (u:GenZProfile)
RETURN count(u) AS profiles;
```

Países:

``` cypher
MATCH (c:Country)
RETURN count(c) AS countries;
```

Relacionamentos:

``` cypher
MATCH ()-[r]->()
RETURN type(r) AS relationship_type,
       count(r) AS total
ORDER BY total DESC;
```

## 20. Nós órfãos

``` cypher
MATCH (p:Platform)
WHERE NOT (p)<-[:USES]-()
RETURN p;
```

``` cypher
MATCH (c:Country)
WHERE NOT (c)<-[:LIVES_IN]-()
RETURN c;
```

## 21. Duplicidade

``` cypher
MATCH (u:GenZProfile)
WITH u.profile_id AS id, count(*) AS total
WHERE total > 1
RETURN id, total;
```

Resultado esperado:

``` text
0 registros
```

## 22. Validação do schema

``` cypher
CALL db.schema.visualization();
```

Salvar a evidência em:

``` text
assets/
```

## 23. Consultas de negócio

Executar:

``` text
cypher/03_business_queries.cypher
```

Perguntas:

1.  Quais plataformas aparecem com maior frequência?
2.  Quais países apresentam maior concentração por plataforma?
3.  Qual finalidade de uso está mais associada a cada plataforma?
4.  Como o uso noturno varia por plataforma?
5.  Como o nível de addiction se distribui entre plataformas?
6.  Quais plataformas apresentam maior média de uso diário?
7.  Como idade e comportamento se relacionam?

## 24. Evidências

Capturar resultados no Neo4j Browser, Workspace ou Explore/Bloom quando
disponível.

Salvar em:

``` text
evidencias/
```

Exemplo:

``` text
evidencias/
├── 01_schema.png
├── 02_platform_usage.png
├── 03_country_platform.png
├── 04_night_usage.png
└── 05_addiction_platform.png
```

Cada evidência deve estar associada a uma query documentada.

## 25. Registro de execução

Registrar:

``` text
Data
Versão dos datasets
Linhas de origem
Linhas carregadas
Nós
Relacionamentos
Queries executadas
Resultado das validações
```

Exemplo:

``` text
Execution date: 2026-08-10
Gen-Z source rows: 1,000,000
Gen-Z graph sample: 10,000
Validation status: PASS
```

## 26. Reprodutibilidade

Uma análise reproduzível exige:

``` text
mesmo dataset
+
mesma transformação
+
mesma configuração
+
mesma versão do código
=
resultado equivalente
```

Registrar:

-   commit Git;
-   versão dos datasets;
-   parâmetros de amostragem;
-   versão Python;
-   versões das bibliotecas;
-   data da execução.

## 27. Controle de alterações

``` bash
git status
git diff
git add .
git commit -m "docs: improve reproducibility documentation"
git push
```

## 28. Checklist

-   [ ] Dataset original obtido.
-   [ ] Schema validado.
-   [ ] Dados processados.
-   [ ] Amostra gerada com seed documentada.
-   [ ] AuraDB Free criada.
-   [ ] Constraints executadas.
-   [ ] Dataset demográfico carregado.
-   [ ] Dataset Gen-Z carregado.
-   [ ] Contagem de nós validada.
-   [ ] Contagem de relacionamentos validada.
-   [ ] Nós órfãos verificados.
-   [ ] Duplicidades verificadas.
-   [ ] `db.schema.visualization()` executado.
-   [ ] Queries de negócio executadas.
-   [ ] Evidências capturadas.
-   [ ] Insights documentados.

## 29. Troubleshooting

### Arquivo não encontrado

Verifique:

``` text
data/raw/
```

e confirme o nome do CSV.

### `LOAD CSV` não acessa o arquivo

Em AuraDB, caminhos locais não são acessíveis pelo servidor.

Utilize URL HTTP/HTTPS acessível ou Data Importer.

### Constraint já existe

Use:

``` cypher
IF NOT EXISTS
```

ou:

``` cypher
SHOW CONSTRAINTS;
```

### Limite de armazenamento

Reduza `sample_size` ou utilize agregações.

Não force a carga de 1 milhão de observações no AuraDB Free.

### Instância pausada

Reative a instância e execute novamente as validações.

## 30. Resultado esperado

Ao final, um terceiro deve conseguir:

``` text
1. criar o banco;
2. preparar os dados;
3. carregar o grafo;
4. validar o schema;
5. executar as queries;
6. reproduzir os insights;
7. entender as limitações;
8. auditar as decisões técnicas.
```

## 31. Critério de sucesso

O sucesso não é apenas:

``` text
"o CSV foi importado."
```

O critério é:

> **um terceiro consegue reproduzir a transformação, reconstruir o
> grafo, validar sua integridade e chegar às mesmas conclusões
> analíticas sob as mesmas premissas.**

Esse é o princípio de reprodutibilidade adotado neste projeto.
