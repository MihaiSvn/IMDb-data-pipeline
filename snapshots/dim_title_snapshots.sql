{% snapshot dim_title_snapshot %}

-- check_cols -> verific coloanele astea daca se modifica si dbt stie sa schimbe automat
{{
    config(
        target_schema='main',
        unique_key='title_id',
        strategy='check',
        check_cols=['primary_title', 'runtime_minutes', 'genres']
    )

}}

select
    title_id,
    primary_title,
    cast(runtime_minutes as integer) as runtime_minutes,
    raw_genres as genres
from {{ ref('stg_title_basics') }}

{% endsnapshot %}
