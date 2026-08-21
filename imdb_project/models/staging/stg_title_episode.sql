select
    tconst as title_id,
    parentTconst as parent_title_id,
    cast(seasonNumber as integer) as season_number,
    cast(episodeNumber as integer) as episode_number


from {{source('imdb_raw','title_episode')}}
