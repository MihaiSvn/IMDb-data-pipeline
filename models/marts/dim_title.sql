--ca as adaug isActive la snapshot

select
    *,
    case
        when dbt_valid_to is null then true
        else false
    end as is_active
from {{ ref('dim_title_snapshot') }}
