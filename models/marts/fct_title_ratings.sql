with ratings as (
    select * from  {{ ref('stg_title_ratings') }}
),

titles as (
    select * from  {{ ref('stg_title_basics') }}
),

final as (
    select r.title_id,
    t.start_year as year_id,
    r.average_rating,
    r.num_votes
    from ratings r
    join titles t on r.title_id=t.title_id
)

select * from final
