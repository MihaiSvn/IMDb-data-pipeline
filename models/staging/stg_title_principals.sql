select

tconst as title_id,
cast(ordering as integer) as ordering,
nconst as name_id,
category,
job,
characters as characters_raw

from {{source('imdb_raw','title_principals')}}
