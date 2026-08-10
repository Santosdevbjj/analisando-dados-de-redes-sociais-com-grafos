# Contexto do projeto

O projeto analisa dados de redes sociais com Neo4j AuraDB Free usando dois conjuntos complementares:

1. **Global Social Media Users by Age Gender 2025**
   - visão macro por plataforma
   - distribuição etária e de gênero
   - leitura de audience mix

2. **Gen-Z Social Media Usage Dataset**
   - 1 milhão de linhas
   - hábitos de uso, saúde mental, tempo de sessão, uso noturno e plataforma principal
   - leitura comportamental com foco em Gen Z

O desenho do projeto usa uma modelagem híbrida para respeitar os limites do plano gratuito:
- nós de baixa cardinalidade viram nós do grafo
- sinais de alta cardinalidade viram propriedades de nós agregados de perfil
