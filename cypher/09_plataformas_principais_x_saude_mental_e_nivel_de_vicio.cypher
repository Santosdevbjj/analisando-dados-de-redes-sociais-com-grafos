MATCH (u:GenZProfile)-[:USES]->(p:Platform)
RETURN p.name AS Plataforma,
       count(u) AS TotalPerfis,
       round(avg(u.avg_daily_usage_hours), 2) AS MediaHorasDiarias,
       round(avg(u.avg_mental_health_score), 2) AS MediaSaudeMental,
       round(avg(u.avg_screen_time_before_sleep), 2) AS MediaTelaPreSonoMin
ORDER BY MediaSaudeMental ASC;
