// ============================================================================
// Database Schema & Constraints Definition
// Arquivo de configuração base para inicialização do Neo4j AuraDB.
// ============================================================================

// Constraints de Unicidade
CREATE CONSTRAINT platform_name_unique IF NOT EXISTS[span_6](start_span)[span_6](end_span)[span_7](start_span)[span_7](end_span)
FOR (p:Platform) REQUIRE p.name IS UNIQUE;[span_8](start_span)[span_8](end_span)[span_9](start_span)[span_9](end_span)

CREATE CONSTRAINT country_name_unique IF NOT EXISTS[span_10](start_span)[span_10](end_span)[span_11](start_span)[span_11](end_span)
FOR (c:Country) REQUIRE c.name IS UNIQUE;[span_12](start_span)[span_12](end_span)[span_13](start_span)[span_13](end_span)

CREATE CONSTRAINT age_group_name_unique IF NOT EXISTS[span_14](start_span)[span_14](end_span)[span_15](start_span)[span_15](end_span)
FOR (a:AgeGroup) REQUIRE a.name IS UNIQUE;[span_16](start_span)[span_16](end_span)[span_17](start_span)[span_17](end_span)

CREATE CONSTRAINT genz_profile_id_unique IF NOT EXISTS[span_18](start_span)[span_18](end_span)[span_19](start_span)[span_19](end_span)
FOR (u:GenZProfile) REQUIRE u.profile_id IS UNIQUE;[span_20](start_span)[span_20](end_span)[span_21](start_span)[span_21](end_span)

// Índices de Busca e Performance
CREATE INDEX idx_genz_age IF NOT EXISTS
FOR (u:GenZProfile) ON (u.age);

CREATE INDEX idx_genz_addiction IF NOT EXISTS
FOR (u:GenZProfile) ON (u.addiction_level);

CREATE INDEX idx_platform_mau IF NOT EXISTS
FOR (p:Platform) ON (p.mau_billion);
