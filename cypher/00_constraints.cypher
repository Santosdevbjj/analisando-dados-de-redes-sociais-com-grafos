/*
Constraints and indexes designed for Neo4j AuraDB Free.
The graph is intentionally hybrid:
- low-cardinality dimensions become nodes
- high-cardinality user signals become properties on UsageProfile nodes
*/

CREATE CONSTRAINT platform_name IF NOT EXISTS
FOR (p:Platform) REQUIRE p.name IS UNIQUE;

CREATE CONSTRAINT country_name IF NOT EXISTS
FOR (c:Country) REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT age_group_label IF NOT EXISTS
FOR (a:AgeGroup) REQUIRE a.label IS UNIQUE;

CREATE CONSTRAINT usage_profile_id IF NOT EXISTS
FOR (u:UsageProfile) REQUIRE u.profile_id IS UNIQUE;
