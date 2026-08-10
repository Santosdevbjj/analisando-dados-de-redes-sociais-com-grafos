// ============================================================================
// 05 --- Validation Queries (Data Quality & Integrity Check)
// Objetivo: Validação pós-carga de integridade, identificação de nós órfãos,
// duplicidades e checagem do schema.
// ============================================================================

// 1. Contagem Geral de Nós por Rótulo[span_0](start_span)[span_0](end_span)
MATCH (n)
RETURN labels(n)[0] AS NodeLabel, count(n) AS TotalNodes
ORDER BY TotalNodes DESC;

// 2. Contagem Geral de Relacionamentos por Tipo[span_1](start_span)[span_1](end_span)
MATCH ()-[r]->()
RETURN type(r) AS RelationshipType, count(r) AS TotalRelationships
ORDER BY TotalRelationships DESC;

// 3. Validação de Perfis Órfãos (Sem conexões com plataformas ou países)[span_2](start_span)[span_2](end_span)
MATCH (u:GenZProfile)
WHERE NOT (u)-[:USES]->(:Platform) OR NOT (u)-[:LIVES_IN]->(:Country)
RETURN count(u) AS TotalOrphanProfiles;

// 4. Validação de Plataformas Órfãs[span_3](start_span)[span_3](end_span)
MATCH (p:Platform)
WHERE NOT (p)<-[:USES]-() AND NOT (p)-[:HAS_DEMOGRAPHIC]->()
RETURN p.name AS UnusedPlatform;

// 5. Checagem de Duplicidades em GenZProfile (IDs Únicos)[span_4](start_span)[span_4](end_span)
MATCH (u:GenZProfile)
WITH u.profile_id AS id, count(*) AS total
WHERE total > 1
RETURN id AS DuplicateID, total AS Ocurrences;

// 6. Visualização do Schema Estrutural do Grafo[span_5](start_span)[span_5](end_span)
CALL db.schema.visualization();
