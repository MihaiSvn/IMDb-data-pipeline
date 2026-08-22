with raw_years as (
    select start_year as y_val
    from {{ ref('stg_title_basics') }}
    where start_year is not null

    union

    select end_year as y_val
    from {{ ref('stg_title_basics') }}
    where end_year is not null
),

final as (
    select
        cast(y_val as integer) as year_id,
        cast(y_val as integer) as year_value
    from raw_years
    where y_val is not null
)

select * from final
order by year_id
