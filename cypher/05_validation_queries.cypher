// ============================================================================
// 05 --- Validation Queries (Data Quality & Integrity Check)
// Objetivo: Validação pós-carga de integridade, identificação de nós órfãos,
// duplicidades e checagem do schema.
// ============================================================================

// 1. Contagem Geral de Nós por Rótulo
MATCH (n)
RETURN labels(n)[0] AS NodeLabel, count(n) AS TotalNodes
ORDER BY TotalNodes DESC;

// 2. Contagem Geral de Relacionamentos por Tipo
MATCH ()-[r]->()
RETURN type(r) AS RelationshipType, count(r) AS TotalRelationships
ORDER BY TotalRelationships DESC;

// 3. Validação de Perfis Órfãos (Sem conexões com plataformas ou países)
MATCH (u:UsageProfile)
WHERE NOT (u)-[:USES_PRIMARY]->(:Platform) OR NOT (u)-[:LOCATED_IN]->(:Country)
RETURN count(u) AS TotalOrphanProfiles;

// 4. Validação de Plataformas Órfãs
MATCH (p:Platform)
WHERE NOT (p)<-[:USES_PRIMARY]-() AND NOT (p)-[:HAS_AUDIENCE]->()
RETURN p.name AS UnusedPlatform;

// 5. Checagem de Duplicidades em UsageProfile (IDs Únicos)
MATCH (u:UsageProfile)
WITH u.profile_id AS id, count(*) AS total
WHERE total > 1
RETURN id AS DuplicateID, total AS Ocurrences;

// 6. Visualização do Schema Estrutural do Grafo
CALL db.schema.visualization();
