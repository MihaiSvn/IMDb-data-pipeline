-- Version 2: Increased vote threshold (min 5 titles, min 500,000 votes combined)
-- Insight: The results are dominated by famous Anime and TV series directors (e.g., Megumi Ishitani) because TV episodes generally receive much higher fan ratings compared to feature films.

SELECT
    p.primary_name AS director_name,
    COUNT(f.title_id) AS total_movies,
    SUM(f.num_votes) AS total_combined_votes,
    ROUND(AVG(f.average_rating), 2) AS avg_director_rating
FROM {{ ref('fct_title_ratings') }} f
JOIN {{ ref('bridge_title_crew') }} b ON f.title_id = b.title_id
JOIN {{ ref('dim_person') }} p ON b.name_id = p.name_id
WHERE b.role = 'director'
GROUP BY p.primary_name
HAVING COUNT(f.title_id) >= 5
   AND SUM(f.num_votes) >= 500000
ORDER BY avg_director_rating DESC
LIMIT 10
