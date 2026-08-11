MATCH (p:Platform)<-[:USES]-(u:GenZProfile)-[:LIVES_IN]->(c:Country)
RETURN p.name AS Plataforma,
       p.mau_billion AS MAUGlobalBilhoes,
       c.name AS Pais,
       sum(u.sample_count) AS AmostraGenZ,
       round(avg(u.avg_daily_usage_hours), 2) AS HorasDiariasGenz
ORDER BY MAUGlobalBilhoes DESC, AmostraGenZ DESC;
