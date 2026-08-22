select
    NULLIF(tconst, '\N') as title_id,
    TRY_CAST(averageRating AS FLOAT) as average_rating,
    TRY_CAST(numVotes AS INTEGER) as num_votes
from {{ source('imdb_raw', 'title_ratings') }}
