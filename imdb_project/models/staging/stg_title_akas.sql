select
titleId as title_id,
cast(ordering as integer) as ordering,
title,
region,
language,
types as types_raw,
attributes as attributes_raw,
cast(isOriginalTitle as boolean) as is_original_title


from {{source('imdb_raw','title_akas')}}
