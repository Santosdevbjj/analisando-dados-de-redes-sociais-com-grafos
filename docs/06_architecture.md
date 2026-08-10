# 06 --- Architecture

## 1. Objetivo

A arquitetura demonstra como dados sociais heterogêneos são
transformados em um modelo de grafo consultável no Neo4j AuraDB Free.

O objetivo não é simplesmente importar CSV, mas construir uma cadeia
reproduzível:

``` text
Dados brutos
    ↓
Validação
    ↓
Normalização
    ↓
Modelagem
    ↓
Carga no Neo4j
    ↓
Validação do grafo
    ↓
Consultas
    ↓
Insights
```

## 2. Visão geral

``` text
┌─────────────────────────────────────────────┐
│ DATA SOURCES                                │
│ Global Social Media Users 2025              │
│ Gen-Z Social Media Usage 1M                │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ DATA PREPARATION                            │
│ Python / Pandas                             │
│ Schema / Types / Sampling / IDs             │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ IMPORT LAYER                                │
│ Processed CSV / Sample CSV                  │
│ HTTP-accessible source for Aura             │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ NEO4J AURADB FREE                           │
│ Constraints / Nodes / Relationships / Cypher│
└──────────────────┬──────────────────────────┘
                   ↓
          ┌────────┴────────┐
          ↓                 ↓
     Validation       Business Queries
                            ↓
                         Insights
```

## 3. Camadas

### Data Source Layer

Fontes:

``` text
Global Social Media Users by Age Gender 2025
Gen-Z Social Media Usage Dataset
```

Arquivos originais grandes não devem ser versionados sem necessidade.

### Data Preparation Layer

Responsável por:

-   leitura;
-   schema;
-   tipos;
-   domínios;
-   percentuais;
-   normalização;
-   IDs;
-   amostras;
-   arquivos processados.

Tecnologias:

``` text
Python
Pandas
```

## 4. Modelo de grafo

``` text
(:GenZProfile)-[:USES]->(:Platform)
(:GenZProfile)-[:LIVES_IN]->(:Country)
(:Platform)-[:HAS_DEMOGRAPHIC]->(:DemographicSegment)
(:DemographicSegment)-[:FOR_AGE_GROUP]->(:AgeGroup)
```

## 5. Modelo lógico

``` text
                         ┌─────────────┐
                         │   Country   │
                         └──────▲──────┘
                                │
                            LIVES_IN
                                │
                         ┌──────┴──────┐
                         │ GenZProfile │
                         └──────┬──────┘
                                │
                              USES
                                │
                                ▼
                         ┌─────────────┐
                         │  Platform   │
                         └──────┬──────┘
                                │
                       HAS_DEMOGRAPHIC
                                │
                                ▼
                    ┌────────────────────┐
                    │DemographicSegment  │
                    └─────────┬──────────┘
                              │
                       FOR_AGE_GROUP
                              │
                              ▼
                        ┌───────────┐
                        │ AgeGroup  │
                        └───────────┘
```

## 6. Controle de cardinalidade

O dataset Gen-Z contém 1 milhão de linhas.

A carga integral pode consumir rapidamente os limites do AuraDB Free.
Por isso:

1.  o dataset completo permanece como fonte;
2.  o grafo de demonstração usa amostra controlada;
3.  perguntas agregadas podem usar dados agregados;
4.  o tamanho efetivamente carregado é documentado.

Exemplo:

``` text
10.000 GenZProfile
≈ 20.000 relationships
```

mais os relacionamentos das dimensões.

## 7. Constraints

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

## 8. Por que Neo4j?

O domínio possui relações naturais entre:

``` text
Observação
   ↓
País
   ↓
Plataforma
   ↓
Faixa etária
   ↓
Demografia
```

No grafo, essas relações são de primeira classe.

Isso permite perguntas como:

> Quais plataformas são mais utilizadas por observações de determinado
> país?

e:

> Quais segmentos demográficos estão associados a uma plataforma?

## 9. Alternativa rejeitada

Uma alternativa seria:

``` text
(:User)
```

com dezenas de propriedades.

Ela seria simples, mas perderia parte do valor relacional.

A separação permite reutilizar entidades como:

``` text
Instagram
TikTok
YouTube
Brazil
USA
```

## 10. Dataset demográfico

O dataset demográfico é agregado.

Portanto, não deve ser modelado como:

``` text
1 nó = 1 usuário real
```

Modelo:

``` text
Platform
    ↓
DemographicSegment
    ↓
AgeGroup
```

## 11. Dataset Gen-Z

Como não existe `user_id`, `GenZProfile` significa:

> observação comportamental sintética

e não identidade persistente.

## 12. Organização das queries

``` text
cypher/
├── 00_constraints.cypher
├── 01_load_global_demographics.cypher
├── 02_load_genz_profiles.cypher
├── 03_business_queries.cypher
├── 04_graph_data_science.cypher
└── 05_validation_queries.cypher
```

## 13. Data Quality

Antes da carga:

``` text
schema
types
nulls
domains
ranges
duplicates
```

Depois da carga:

``` text
node counts
relationship counts
orphan nodes
duplicate entities
missing relationships
```

## 14. Observabilidade

Registrar:

``` text
dataset
rows_read
rows_loaded
rows_rejected
nodes_created
relationships_created
validation_status
```

## 15. Segurança

Nunca versionar:

``` text
NEO4J_URI
NEO4J_USERNAME
NEO4J_PASSWORD
API keys
tokens
.env
```

Usar `.env.example` sem valores reais.

## 16. Limitações do AuraDB Free

A arquitetura não assume:

-   múltiplas instâncias simultâneas;
-   armazenamento ilimitado;
-   backups contínuos;
-   execução permanente;
-   grandes cargas sem controle.

## 17. Evolução para produção

``` text
Object Storage
      ↓
Data Lake
      ↓
ETL / ELT
      ↓
Neo4j Enterprise / Aura
      ↓
Graph Data Science
      ↓
API
      ↓
Dashboard
```

Possíveis extensões:

-   pipelines incrementais;
-   data lineage;
-   monitoramento;
-   CI/CD;
-   testes automatizados;
-   GDS;
-   APIs;
-   dashboards.

## 18. Trade-offs

  -----------------------------------------------------------------------
  Decisão                 Benefício               Trade-off
  ----------------------- ----------------------- -----------------------
  Amostragem              Respeita Aura Free      Não representa 1M no
                                                  grafo

  Nós de referência       Reuso e travessia       Modelo mais complexo

  `GenZProfile` técnico   Preserva observações    Não representa usuários
                                                  reais

  Cypher separado         Manutenção              Mais arquivos

  Dados agregados         Integridade             Menor conexão direta
  separados                                       com perfis

  Sem credenciais no Git  Segurança               Configuração manual
  -----------------------------------------------------------------------

## 19. Princípio arquitetural

> **O modelo deve representar a realidade dos dados, e não forçar os
> dados a caberem em um modelo previamente escolhido.**
