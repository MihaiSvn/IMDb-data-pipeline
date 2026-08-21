select
    tconst as title_id,
    cast(averageRating as float) as average_rating,
    cast(numVotes as integer) as num_votes

from {{ source('imdb_raw', 'title_ratings') }}
