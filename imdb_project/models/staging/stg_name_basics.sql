select
    nconst as name_id,
    primaryName as primary_name,
    cast(birthYear as integer) as birth_year,
    cast(deathYear as integer) as death_year,
    primaryProfession as primary_profession,
    knownForTitles as known_for_titles_raw



from {{source('imdb_raw','name_basics')}}
