select
    tconst as title_id,
    directors as directors_raw,
    writers as writers_raw

from {{source('imdb_raw','title_crew')}}
