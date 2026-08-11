/*
Load the aggregated Gen-Z profiles.
This file is designed for AuraDB Free, keeping the graph under the 200k node / 400k relationship limits.

*/

:param genz_url => 'https://raw.githubusercontent.com/Santosdevbjj/analisando-dados-de-redes-sociais-com-grafos/main/data/processed/genz_usage_profiles.csv';


LOAD CSV WITH HEADERS FROM $genz_url AS row
MERGE (u:UsageProfile {profile_id: row.profile_id})
SET u.age = toInteger(row.age),
    u.gender = row.gender,
    u.country = row.country,
    u.primary_platform = row.primary_platform,
    u.purpose = row.purpose,
    u.addiction_level = row.addiction_level,
    u.num_platforms_used = toInteger(row.num_platforms_used),
    u.night_usage = toInteger(row.night_usage),
    u.sample_count = toInteger(row.sample_count),
    u.avg_daily_usage_hours = toFloat(row.avg_daily_usage_hours),
    u.avg_session_minutes = toFloat(row.avg_session_minutes),
    u.avg_mental_health_score = toFloat(row.avg_mental_health_score),
    u.avg_screen_time_before_sleep = toFloat(row.avg_screen_time_before_sleep)

MERGE (p:Platform {name: row.primary_platform})
MERGE (c:Country {name: row.country})

MERGE (u)-[:USES_PRIMARY]->(p)
MERGE (u)-[:LOCATED_IN]->(c);
