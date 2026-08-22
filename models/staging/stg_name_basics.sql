select
    NULLIF(nconst, '\N') as name_id,
    NULLIF(primaryName, '\N') as primary_name,
    NULLIF(birthYear, '\N')::INT as birth_year,
    NULLIF(deathYear, '\N')::INT as death_year,
    NULLIF(primaryProfession, '\N') as primary_profession,
    NULLIF(knownForTitles, '\N') as known_for_titles_raw
from {{source('imdb_raw','name_basics')}}
