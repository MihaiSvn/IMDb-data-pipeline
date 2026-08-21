select
    title_id,

    unnest(string_split(writers_raw, ',')) as writer_id

from {{ ref('stg_title_crew') }}
where writers_raw is not null
