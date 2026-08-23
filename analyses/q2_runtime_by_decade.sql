-- Has the average movie runtime changed by decade, and does runtime correlate with rating?
SELECT
    {{ get_decade('y.year_value') }} AS decade,
    COUNT(f.title_id) AS total_movies,
    ROUND(AVG(t.runtime_minutes), 2) AS avg_runtime,
    ROUND(CORR(f.average_rating, t.runtime_minutes), 4) AS runtime_rating_correlation
FROM {{ ref('fct_title_ratings') }} f
JOIN {{ ref('dim_title_snapshot') }} t ON f.title_id = t.title_id
JOIN {{ ref('dim_year') }} y ON f.year_id = y.year_id
JOIN {{ ref('stg_title_basics') }} stg ON f.title_id = stg.title_id
WHERE t.runtime_minutes IS NOT NULL
  AND t.dbt_valid_to IS NULL
  AND y.year_value IS NOT NULL
  AND stg.title_type = 'movie'
GROUP BY 1
ORDER BY 1 ASC
