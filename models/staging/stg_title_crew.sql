select
    NULLIF(tconst, '\N') as title_id,
    NULLIF(directors, '\N') as directors_raw,
    NULLIF(writers, '\N') as writers_raw
from {{source('imdb_raw','title_crew')}}
