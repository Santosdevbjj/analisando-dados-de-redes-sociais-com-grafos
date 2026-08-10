# Troubleshooting

## 1. CSV demográfico global com linhas irregulares
O arquivo `Global Social Media Users by Age-Gender 2025.zip` possui linhas com campos de nota que quebram a leitura padrão.
Solução:
- ler com `csv.reader`
- normalizar linhas com mais ou menos colunas
- reconstruir a última coluna como texto livre

## 2. Limite do AuraDB Free
O plano gratuito suporta até 200.000 nós e 400.000 relacionamentos.
Solução:
- não modelar 1 milhão de usuários como nós individuais
- agregar o dataset Gen-Z em perfis analíticos
- armazenar sinais contínuos como propriedades

## 3. Importação no Aura
AuraDB trabalha melhor com fontes remotas `http(s)` ou com Data Importer.
Solução:
- publicar os CSVs processados no próprio GitHub
- usar URLs raw no `LOAD CSV`
- ou importar os CSVs via Neo4j Data Importer
