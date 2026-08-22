select
    NULLIF(titleId, '\N') as title_id,
    NULLIF(ordering, '\N')::INT as ordering,
    NULLIF(title, '\N') as title,
    NULLIF(region, '\N') as region,
    NULLIF(language, '\N') as language,
    NULLIF(types, '\N') as types_raw,
    NULLIF(attributes, '\N') as attributes_raw,
    NULLIF(isOriginalTitle, '\N')::INT::BOOLEAN as is_original_title
from {{source('imdb_raw','title_akas')}}
