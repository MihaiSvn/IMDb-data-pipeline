select
    title_id,

    unnest(string_split(directors_raw, ',')) as director_id

from {{ ref('stg_title_crew') }}
where directors_raw is not null
