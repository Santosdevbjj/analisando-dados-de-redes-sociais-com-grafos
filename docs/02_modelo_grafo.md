# Modelo do grafo

## Nós
- `:Platform`
- `:AgeGroup`
- `:Country`
- `:UsageProfile`

## Relacionamentos
- `(:Platform)-[:HAS_AUDIENCE]->(:AgeGroup)`
- `(:UsageProfile)-[:USES_PRIMARY]->(:Platform)`
- `(:UsageProfile)-[:LOCATED_IN]->(:Country)`

## Decisão de modelagem
O conjunto Gen-Z possui 1 milhão de registros. Em vez de criar um nó para cada linha, o projeto agrega registros por perfil analítico:
- idade
- gênero
- país
- plataforma principal
- propósito
- nível de addiction
- número de plataformas usadas
- uso noturno

Isso reduz drasticamente o volume de nós/relacionamentos e deixa o modelo compatível com AuraDB Free.
