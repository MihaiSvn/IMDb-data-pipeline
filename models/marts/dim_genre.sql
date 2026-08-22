with unique_genres as (
    select distinct
        trim(genre) as genre_name
    from {{ ref('int_title_genres') }}
    where trim(genre) != ''
),

final as (
    select
        {{ dbt_utils.generate_surrogate_key(['genre_name']) }} as genre_id,
        genre_name
    from unique_genres
)

select * from final
order by genre_id
