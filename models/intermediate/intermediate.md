# The `_raw` Columns Breakdown

*   **`raw_genres`** *(from stg_title_basics)*
    *   Unnested (`int_title_genres`).
    *   **Why:** Required to analyze genre-specific metrics.

*   **`directors_raw` & `writers_raw`** *(from stg_title_crew)*
    *   Unnested (`int_title_directors`, `int_title_writers`).
    *   **Why:** Required to group by individual director or writer in order to rank the best creators based on their production history and average ratings.
*   **`known_for_titles_raw`** *(from stg_name_basics)*
    *   Ignored.
    *   **Why:** `stg_title_principals` already acts as the primary, detailed bridge table.

*   **`characters_raw`** *(from stg_title_principals)*
    *   Ignored.
    *   **Why:** Not required for the current metrics.

*   **`types_raw` & `attributes_raw`** *(from stg_title_akas)*
    *   Ignored.
    *   **Why:** Not required for the current metrics.
