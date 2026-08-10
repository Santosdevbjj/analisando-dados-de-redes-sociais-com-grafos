/*
Load the cleaned global demographic dataset.
Recommended import source:
- GitHub raw URL for data/processed/global_social_media_users_clean.csv
- Or upload the CSV in Neo4j Data Importer

:param global_url => 'https://raw.githubusercontent.com/Santosdevbjj/analisando-dados-de-redes-sociais-com-grafos/main/data/processed/global_social_media_users_clean.csv';
*/

LOAD CSV WITH HEADERS FROM $global_url AS row
MERGE (p:Platform {name: row.Platform})
SET p.mau_billion = toFloat(row.mau_billion),
    p.overall_female_pct = toFloat(row.overall_female_pct),
    p.overall_male_pct = toFloat(row.overall_male_pct),
    p.trend_notes = coalesce(row.`Key Trends / Notes`, '')

MERGE (a:AgeGroup {label: row.`Age Group`})
SET a.sort_order = CASE row.`Age Group`
    WHEN '10-19' THEN 10
    WHEN '13-17' THEN 13
    WHEN '18-24' THEN 18
    WHEN '25-34' THEN 25
    WHEN '35-44' THEN 35
    WHEN '45-54' THEN 45
    WHEN '55-64' THEN 55
    WHEN '55+' THEN 55
    WHEN '65+' THEN 65
    ELSE 999
END

MERGE (p)-[r:HAS_AUDIENCE]->(a)
SET r.female_pct = CASE
        WHEN row.`% Female Users (within age group)` IN ['N/A', '', null] THEN null
        ELSE toFloat(replace(row.`% Female Users (within age group)`, '%', ''))
    END,
    r.male_pct = CASE
        WHEN row.`% Male Users (within age group)` IN ['N/A', '', null] THEN null
        ELSE toFloat(replace(row.`% Male Users (within age group)`, '%', ''))
    END,
    r.notes = coalesce(row.`Key Trends / Notes`, '');
