{% macro get_decade(year_column) %}

    -- pt intrebarea has the average movie runtime changed by decade, schimb  anul in deceniu
    -- folosesc // ca sa nu imi iasa cu virgula, sa fie ca in c++ sau alte limbaje
    -- 2005/10=200 -> -> 200* 10=2000
    cast(( {{ year_column }} // 10 )*10 as integer)

{% endmacro %}
