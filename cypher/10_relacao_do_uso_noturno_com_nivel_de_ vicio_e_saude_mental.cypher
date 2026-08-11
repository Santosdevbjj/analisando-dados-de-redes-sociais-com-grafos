MATCH (u:GenZProfile)
RETURN CASE u.night_usage WHEN 1 THEN 'Uso Noturno (Sim)' ELSE 'Uso Noturno (Não)' END AS HabitoNoturno,
       u.addiction_level AS NivelVicio,
       sum(u.sample_count) AS TotalJovensRepresentados,
       round(avg(u.avg_daily_usage_hours), 2) AS HorasDiarias,
       round(avg(u.avg_mental_health_score), 2) AS ScoreSaudeMental
ORDER BY HabitoNoturno, NivelVicio;
