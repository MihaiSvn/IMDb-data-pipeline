-- Version 3: Final refinement (filtered strictly for 'movie' title_type)
-- Insight: By joining with the staging layer and filtering for feature films only, we successfully extract the true top Hollywood/cinema directors.

SELECT
    p.primary_name AS director_name,
    COUNT(f.title_id) AS total_movies,
    SUM(f.num_votes) AS total_combined_votes,
    ROUND(AVG(f.average_rating), 2) AS avg_director_rating
FROM {{ ref('fct_title_ratings') }} f
JOIN {{ ref('bridge_title_crew') }} b ON f.title_id = b.title_id
JOIN {{ ref('dim_person') }} p ON b.name_id = p.name_id
JOIN {{ ref('stg_title_basics') }} stg ON f.title_id = stg.title_id
WHERE b.role = 'director'
  AND stg.title_type = 'movie'
GROUP BY p.primary_name
HAVING COUNT(f.title_id) >= 5
   AND SUM(f.num_votes) >= 500000
ORDER BY avg_director_rating DESC
LIMIT 10
