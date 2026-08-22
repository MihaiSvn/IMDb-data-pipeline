{% test not_in_future(model, column_name) %}
    select *
    from {{ model }}
    where {{ column_name }} > extract(year from current_date)
{% endtest %}
