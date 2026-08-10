// ============================================================================
// 04 --- Graph Data Science (GDS) Analytics
// Objetivo: Projeções de memória de grafos, métricas de centralidade e detecção
// de comunidades (Louvain / FastRP) para análise comportamental da Gen-Z.
// ============================================================================

// 1. Verificar disponibilidade da biblioteca GDS
CALL gds.version();

// 2. Limpar projeções existentes (se houver)
CALL gds.graph.drop('genz-usage-projection', false);

// 3. Criar a Projeção de Grafo em Memória (Bipartida: GenZProfile + Platform)
CALL gds.graph.project(
  'genz-usage-projection',
  ['GenZProfile', 'Platform'],
  {
    USES: {
      type: 'USES',
      orientation: 'UNDIRECTED',
      properties: ['avg_session_minutes', 'daily_usage_hours']
    }
  }
);

// 4. Executar Degree Centrality (Identificar plataformas mais centralizadas)
CALL gds.degree.stream('genz-usage-projection')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS Entidade,
       labels(gds.util.asNode(nodeId))[0] AS Tipo,
       score AS GrausConexao
ORDER BY GrausConexao DESC
LIMIT 15;

// 5. Executar Louvain Community Detection (Descobrimento de clusters)
CALL gds.louvain.stream('genz-usage-projection')
YIELD nodeId, communityId
WITH gds.util.asNode(nodeId) AS node, communityId
WHERE node:GenZProfile
RETURN communityId AS ClusterID,
       count(node) AS TotalMembros,
       avg(node.daily_usage_hours) AS MediaUsoDiario,
       avg(node.mental_health_score) AS MediaSaudeMental
ORDER BY TotalMembros DESC
LIMIT 10;

// 6. Limpeza da projeção em memória pós-execução
CALL gds.graph.drop('genz-usage-projection');
