# Dados do projeto

Os arquivos completos dos ZIPs do Kaggle não são versionados aqui por tamanho.

## O que fica neste repositório
- Amostras limpas para validação rápida.
- Scripts para recriar os datasets processados a partir dos ZIPs originais.
- Estrutura pronta para upload no Neo4j AuraDB Free.

## Onde colocar os arquivos originais
Coloque os ZIPs baixados do Kaggle em:

- `data/raw/Global Social Media Users by Age-Gender 2025.zip`
- `data/raw/Gen-Z Social Media Usage Dataset.zip`

Depois execute `python scripts/prepare_datasets.py`.
