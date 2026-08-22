select
    NULLIF(tconst, '\N') as title_id,
    NULLIF(ordering, '\N')::INT as ordering,
    NULLIF(nconst, '\N') as name_id,
    NULLIF(category, '\N') as category,
    NULLIF(job, '\N') as job,
    NULLIF(characters, '\N') as characters_raw
from {{source('imdb_raw','title_principals')}}
