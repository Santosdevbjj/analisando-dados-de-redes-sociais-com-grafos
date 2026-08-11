// ============================================================================
// 06 --- Constraints e Índices de Performance
// ============================================================================

CREATE CONSTRAINT platform_name_unique IF NOT EXISTS
FOR (p:Platform) REQUIRE p.name IS UNIQUE;

CREATE CONSTRAINT age_group_label_unique IF NOT EXISTS
FOR (a:AgeGroup) REQUIRE a.label IS UNIQUE;

CREATE CONSTRAINT country_name_unique IF NOT EXISTS
FOR (c:Country) REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT genz_profile_id_unique IF NOT EXISTS
FOR (u:GenZProfile) REQUIRE u.profile_id IS UNIQUE;

CREATE INDEX idx_genz_addiction IF NOT EXISTS
FOR (u:GenZProfile) ON (u.addiction_level);

CREATE INDEX idx_genz_age IF NOT EXISTS
FOR (u:GenZProfile) ON (u.age);
