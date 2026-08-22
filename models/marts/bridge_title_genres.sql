with title_genres as (

    select
        title_id,
        trim(genre) as genre_name
    from {{ ref('int_title_genres') }}
    where trim(genre) != ''
),

genres as (
    select genre_id, genre_name from {{ ref('dim_genre') }}
),

final as (
    select
        tg.title_id,
        dg.genre_id
    from title_genres tg
    join dim_genre dg on tg.genre_name = dg.genre_name
)

select * from final
