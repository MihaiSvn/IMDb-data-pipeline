-- Which genres have the highest ratio of “hidden gems” versus “overrated” titles?
WITH categorized AS (
    SELECT
        g.genre_name,
        CASE
            WHEN f.average_rating >= 7.5 AND f.num_votes BETWEEN 1000 AND 10000 THEN 1
            ELSE 0
        END AS is_hidden_gem,
        CASE
            WHEN f.average_rating <= 6.0 AND f.num_votes > 50000 THEN 1
            ELSE 0
        END AS is_overrated
    FROM {{ ref('fct_title_ratings') }} f
    JOIN {{ ref('bridge_title_genres') }} bg ON f.title_id = bg.title_id
    JOIN {{ ref('dim_genre') }} g ON bg.genre_id = g.genre_id
    JOIN {{ ref('stg_title_basics') }} stg ON f.title_id = stg.title_id
WHERE stg.title_type = 'movie'
)
SELECT
    genre_name,
    SUM(is_hidden_gem) AS hidden_gems,
    SUM(is_overrated) AS overrated,
    ROUND(SUM(is_hidden_gem)::FLOAT / NULLIF(SUM(is_overrated), 0), 2) AS gem_to_overrated_ratio
FROM categorized
GROUP BY genre_name
HAVING SUM(is_hidden_gem) > 10 AND SUM(is_overrated) > 0
ORDER BY gem_to_overrated_ratio DESC
