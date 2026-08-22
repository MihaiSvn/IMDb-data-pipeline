select
    NULLIF(tconst, '\N') as title_id,
    NULLIF(titleType, '\N') as title_type,
    NULLIF(primaryTitle, '\N') as primary_title,
    NULLIF(originalTitle, '\N') as original_title,
    NULLIF(isAdult, '\N')::INT::BOOLEAN as is_adult,
    NULLIF(startYear, '\N')::INT as start_year,
    NULLIF(endYear, '\N')::INT as end_year,
    NULLIF(runtimeMinutes, '\N')::INT as runtime_minutes,
    NULLIF(genres, '\N') as raw_genres
from {{ source('imdb_raw', 'title_basics') }}
