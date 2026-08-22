with persons as (
    select * from {{ ref('stg_name_basics') }}
),

final as (
    select
        name_id,
        primary_name,
        birth_year
    from persons
)

select * from final
