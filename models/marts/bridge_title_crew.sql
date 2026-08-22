with writers as (
    select
        title_id,
        writer_id as name_id,
        'writer' as role
    from {{ ref('int_title_writers') }}
),

directors as (
    select
        title_id,
        director_id as name_id,
        'director' as role
    from {{ ref('int_title_directors') }}
),

final as (

    select * from writers

    union all

    select * from directors
)

select * from final
