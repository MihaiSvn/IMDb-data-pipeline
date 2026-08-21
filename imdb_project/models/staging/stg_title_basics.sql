select
    tconst as title_id,
    titleType as title_type,
    primaryTitle as primary_title,
    originalTitle as original_title,

    cast(isAdult as boolean) as is_adult,
    cast(startYear as integer) as start_year,
    cast(endYear as integer) as end_year,
    cast(runtimeMinutes as integer) as runtime_minutes,

    genres as raw_genres
from {{ source('imdb_raw', 'title_basics') }}
