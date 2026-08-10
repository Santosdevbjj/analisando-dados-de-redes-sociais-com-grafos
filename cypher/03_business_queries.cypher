/*
Business questions answered by the graph
*/

-- 1) Which platforms have the highest MAU and strongest youth share?
MATCH (p:Platform)-[r:HAS_AUDIENCE]->(a:AgeGroup)
WITH p, sum(coalesce(r.female_pct, 0) + coalesce(r.male_pct, 0)) AS youth_signal
RETURN p.name AS platform, p.mau_billion AS mau_billion, youth_signal
ORDER BY mau_billion DESC, youth_signal DESC;

-- 2) Which age groups are strongest for each platform?
MATCH (p:Platform)-[r:HAS_AUDIENCE]->(a:AgeGroup)
RETURN p.name AS platform, a.label AS age_group, r.female_pct, r.male_pct, r.notes
ORDER BY p.name, a.sort_order;

-- 3) Which Gen-Z profiles are most intense in use?
MATCH (u:UsageProfile)
RETURN u.country, u.primary_platform, u.purpose, u.addiction_level,
       u.sample_count, u.avg_daily_usage_hours, u.avg_session_minutes,
       u.avg_mental_health_score, u.avg_screen_time_before_sleep
ORDER BY u.sample_count DESC
LIMIT 25;

-- 4) Which country/platform combinations are most associated with heavier usage?
MATCH (u:UsageProfile)-[:LOCATED_IN]->(c:Country),
      (u)-[:USES_PRIMARY]->(p:Platform)
RETURN c.name AS country, p.name AS platform,
       avg(u.avg_daily_usage_hours) AS avg_daily_usage_hours,
       avg(u.avg_session_minutes) AS avg_session_minutes,
       avg(u.avg_screen_time_before_sleep) AS avg_screen_time_before_sleep,
       avg(u.avg_mental_health_score) AS avg_mental_health_score,
       sum(u.sample_count) AS population
ORDER BY population DESC, avg_daily_usage_hours DESC
LIMIT 25;

-- 5) How does addiction level relate to usage and mental health?
MATCH (u:UsageProfile)
RETURN u.addiction_level AS addiction_level,
       avg(u.avg_daily_usage_hours) AS avg_daily_usage_hours,
       avg(u.avg_session_minutes) AS avg_session_minutes,
       avg(u.avg_mental_health_score) AS avg_mental_health_score,
       avg(u.avg_screen_time_before_sleep) AS avg_screen_time_before_sleep,
       sum(u.sample_count) AS population
ORDER BY
    CASE u.addiction_level
        WHEN 'Low' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'High' THEN 3
        ELSE 99
    END;
