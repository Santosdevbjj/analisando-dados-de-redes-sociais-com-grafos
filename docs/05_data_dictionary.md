# 05 --- Data Dictionary

## 1. Visão geral

Este documento descreve os dados utilizados no projeto **Analisando
Dados de Redes Sociais com Grafos**, incluindo origem, granularidade,
significado das colunas, tipos esperados, regras de qualidade e
mapeamento para o modelo de grafo Neo4j.

O projeto utiliza dois datasets obtidos do Kaggle:

1.  **Global Social Media Users by Age Gender 2025**
2.  **Gen-Z Social Media Usage Dataset**

Os datasets possuem naturezas diferentes:

-   o primeiro é **demográfico e agregado por plataforma/faixa etária**;
-   o segundo é **comportamental e sintético**, com **1.000.000 de
    observações**.

Essa distinção é fundamental para preservar a granularidade correta.

## 2. Fontes de dados

  ------------------------------------------------------------------------------------------
  Dataset          Arquivo original                   Granularidade                Registros
  ---------------- ---------------------------------- ---------------- ---------------------
  Global Social    `social_media_demographics.csv`    Plataforma ×                 85 linhas
  Media Users by                                      faixa etária     
  Age Gender 2025                                                      

  Gen-Z Social     `genz_social_media_usage_1M.csv`   Observação                   1.000.000
  Media Usage                                         comportamental   
  Dataset                                                              
  ------------------------------------------------------------------------------------------

> O dataset Gen-Z não possui identificador explícito de usuário. Cada
> linha deve ser tratada como uma observação sintética, e não como uma
> identidade persistente.

## 3. Global Social Media Users by Age Gender 2025

### 3.1 Granularidade

Cada registro representa uma combinação:

``` text
Platform + Age Group
```

A plataforma aparece em várias linhas porque possui várias faixas
etárias.

O valor de usuários mensais ativos é associado à plataforma. Portanto,
**não deve ser somado linha a linha por faixa etária** sem uma regra
específica de distribuição.

### 3.2 Dicionário de campos

  --------------------------------------------------------------------------------------------------------
  Campo                                    Tipo              Descrição         Uso no grafo
  ---------------------------------------- ----------------- ----------------- ---------------------------
  `Platform`                               string            Nome da           `(:Platform).name`
                                                             plataforma        

  `Total Monthly Active Users (Billion)`   string/decimal    Estimativa de MAU `(:Platform).mau_billion`
                                                             em bilhões        

  `Age Group`                              string            Faixa etária      `(:AgeGroup).name`

  `% Female Users (within age group)`      string            Percentual        `(:DemographicSegment)`
                                                             feminino na faixa 

  `% Male Users (within age group)`        string            Percentual        `(:DemographicSegment)`
                                                             masculino na      
                                                             faixa             

  `Overall % Female Users`                 string            Percentual        `(:Platform).female_pct`
                                                             feminino global   

  `Overall % Male Users`                   string            Percentual        `(:Platform).male_pct`
                                                             masculino global  

  `Key Trends / Notes`                     string            Observações       documentação/atributo
                                                             qualitativas      
  --------------------------------------------------------------------------------------------------------

### 3.3 Valores não numéricos

O dataset contém `N/A`, `High`, `Lower`, `Lowest`, `Similar` e frases
qualitativas.

Não converter esses valores automaticamente para zero.

Regra:

-   percentuais numéricos → número;
-   `N/A` → `null`;
-   expressões qualitativas → texto;
-   estimativas textuais → preservar o original e, quando possível,
    criar campo numérico separado;
-   contexto como `(US)`, `(China)` e `(Japan)` deve ser preservado.

Exemplo:

``` text
"43.2%" → 43.2
"N/A" → null
"(Lower)" → null + anotação textual
```

## 4. Gen-Z Social Media Usage Dataset

### 4.1 Granularidade

Cada linha representa uma **observação comportamental sintética**.

Não existe `user_id` original. Portanto, não é permitido afirmar que
duas linhas pertencem ao mesmo usuário.

### 4.2 Dicionário de campos

  ----------------------------------------------------------------------------------
  Campo                        Tipo              Faixa/valores     Descrição
                                                 observados        
  ---------------------------- ----------------- ----------------- -----------------
  `age`                        integer           13--27            Idade

  `gender`                     categorical       Male, Female,     Gênero
                                                 Other             

  `country`                    categorical       Australia, USA,   País
                                                 India, Germany,   
                                                 Brazil, Canada,   
                                                 UK                

  `daily_usage_hours`          float             0.5--10.0         Horas de uso
                                                                   diário

  `primary_platform`           categorical       Snapchat,         Plataforma
                                                 Twitter, TikTok,  principal
                                                 YouTube,          
                                                 Instagram         

  `num_platforms_used`         integer           1--5              Número de
                                                                   plataformas

  `purpose`                    categorical       Education,        Finalidade
                                                 Socializing,      
                                                 Entertainment,    
                                                 News, Content     
                                                 Creation          

  `avg_session_minutes`        float             aproximadamente   Duração média da
                                                 5--80.26          sessão

  `night_usage`                binary            0, 1              Uso noturno

  `mental_health_score`        float             1--10             Score sintético

  `addiction_level`            categorical       Low, Medium, High Nível sintético

  `screen_time_before_sleep`   float             0--aprox. 138     Tempo de tela
                                                                   antes de dormir
  ----------------------------------------------------------------------------------

## 5. Regras de qualidade

### 5.1 Completude

A inspeção do arquivo de 1 milhão de linhas não identificou valores
nulos nas 12 colunas.

Mesmo assim, a pipeline deve sempre validar nulos em novas execuções.

### 5.2 Domínios categóricos

`gender`:

``` text
Male
Female
Other
```

`country`:

``` text
Australia
USA
India
Germany
Brazil
Canada
UK
```

`primary_platform`:

``` text
Snapchat
Twitter
TikTok
YouTube
Instagram
```

`purpose`:

``` text
Education
Socializing
Entertainment
News
Content Creation
```

`addiction_level`:

``` text
Low
Medium
High
```

`night_usage`:

``` text
0
1
```

## 6. Regras de integridade numérica

``` text
13 <= age <= 27
0.5 <= daily_usage_hours <= 10
1 <= num_platforms_used <= 5
avg_session_minutes > 0
night_usage ∈ {0,1}
1 <= mental_health_score <= 10
screen_time_before_sleep >= 0
```

Esses limites descrevem os dados observados, não regras universais sobre
comportamento humano.

## 7. Mapeamento para o grafo

Entidades:

``` text
(:Platform)
(:Country)
(:GenZProfile)
(:AgeGroup)
(:DemographicSegment)
```

### GenZProfile

Representa uma observação comportamental.

Propriedades:

``` text
profile_id
age
gender
daily_usage_hours
num_platforms_used
purpose
avg_session_minutes
night_usage
mental_health_score
addiction_level
screen_time_before_sleep
source
```

### Platform

``` text
name
mau_billion
female_pct
male_pct
source
```

### Country

``` text
name
```

### AgeGroup

``` text
name
```

### DemographicSegment

Representa:

``` text
Platform + AgeGroup
```

Pode armazenar:

``` text
female_pct_age_group
male_pct_age_group
key_trend
source
```

## 8. Relacionamentos

``` text
(:GenZProfile)-[:USES]->(:Platform)
(:GenZProfile)-[:LIVES_IN]->(:Country)
(:Platform)-[:HAS_DEMOGRAPHIC]->(:DemographicSegment)
(:DemographicSegment)-[:FOR_AGE_GROUP]->(:AgeGroup)
```

`USES` representa a plataforma principal declarada na observação, não
uso exclusivo.

## 9. Chaves

Como não existe `user_id`, gerar um ID técnico determinístico:

``` text
genz_00000001
genz_00000002
...
```

Esse ID não representa identidade real.

Para o dataset demográfico, usar:

``` text
platform_name + age_group
```

Exemplo:

``` text
Instagram|18-24
```

## 10. Proveniência

Quando possível, manter:

``` text
source_dataset
source_file
source_version
```

Exemplo:

``` text
source_dataset = "Gen-Z Social Media Usage Dataset"
source_file = "genz_social_media_usage_1M.csv"
```

## 11. Limitações

1.  O dataset Gen-Z é sintético.
2.  Não existe identificador persistente de usuário.
3.  Não há relações explícitas de amizade/seguidores.
4.  Não existe histórico temporal por usuário.
5.  O dataset demográfico contém estimativas e textos qualitativos.
6.  Plataformas podem usar metodologias diferentes.
7.  Os resultados não demonstram causalidade.

## 12. Regra de ouro

> **Não transformar uma estimativa agregada em uma observação
> individual.**

Os datasets podem ser relacionados conceitualmente por `Platform`, mas
não devem ser tratados como se representassem as mesmas pessoas.
