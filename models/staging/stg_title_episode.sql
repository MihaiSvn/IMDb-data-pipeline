select
    NULLIF(tconst, '\N') as title_id,
    NULLIF(parentTconst, '\N') as parent_title_id,
    NULLIF(seasonNumber, '\N')::INT as season_number,
    NULLIF(episodeNumber, '\N')::INT as episode_number
from {{source('imdb_raw','title_episode')}}
