select

    title_id,
    --string split separa intr o lista adevarata, unnest face un rand pt fiecare
    unnest(string_split(raw_genres, ',')) as genre

from {{ref('stg_title_basics')}}
where raw_genres is not null
