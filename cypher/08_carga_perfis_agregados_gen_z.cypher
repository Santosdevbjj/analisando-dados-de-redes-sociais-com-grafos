// ============================================================================
// 08 --- Carga de Perfis Agregados Gen-Z
// ============================================================================

WITH 'https://raw.githubusercontent.com/Santosdevbjj/analisando-dados-de-redes-sociais-com-grafos/main/data/samples/genz_profile_aggregation_sample_500.csv' AS genz_url

LOAD CSV WITH HEADERS FROM genz_url AS row
WITH row WHERE row.primary_platform IS NOT NULL AND row.country IS NOT NULL

MERGE (c:Country {name: trim(row.country)})
MERGE (p:Platform {name: trim(row.primary_platform)})

WITH row, c, p, 
     "P-" + row.age + "-" + replace(trim(row.gender), " ", "") + "-" + replace(trim(row.country), " ", "") + "-" + replace(trim(row.primary_platform), " ", "") + "-" + replace(trim(row.purpose), " ", "") + "-" + replace(trim(row.addiction_level), " ", "") + "-" + row.num_platforms_used + "-" + row.night_usage AS profileId

MERGE (u:GenZProfile {profile_id: profileId})
SET u.age = toInteger(row.age),
    u.gender = trim(row.gender),
    u.purpose = trim(row.purpose),
    u.addiction_level = trim(row.addiction_level),
    u.num_platforms_used = toInteger(row.num_platforms_used),
    u.night_usage = toInteger(row.night_usage),
    u.sample_count = toInteger(row.sample_count),
    u.avg_daily_usage_hours = toFloat(row.avg_daily_usage_hours),
    u.avg_session_minutes = toFloat(row.avg_session_minutes),
    u.avg_mental_health_score = toFloat(row.avg_mental_health_score),
    u.avg_screen_time_before_sleep = toFloat(row.avg_screen_time_before_sleep)

MERGE (u)-[:LIVES_IN]->(c)

MERGE (u)-[r:USES]->(p)
SET r.is_primary = true,
    r.avg_daily_hours = toFloat(row.avg_daily_usage_hours),
    r.avg_session_mins = toFloat(row.avg_session_minutes);

// Conectar dinamicamente o perfil GenZ à sua faixa etária correspondente
MATCH (u:GenZProfile), (a:AgeGroup)
WHERE (u.age >= 13 AND u.age <= 17 AND a.label = '13-17')
   OR (u.age >= 18 AND u.age <= 24 AND a.label = '18-24')
   OR (u.age >= 25 AND u.age <= 34 AND a.label = '25-34')
MERGE (u)-[:BELONGS_TO]->(a);
