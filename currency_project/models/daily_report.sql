select
    currency,
    rate,
    loaded_at,
    round(rate - lag(rate) over (
        partition by currency 
        order by loaded_at
    ), 4) as rate_change
from {{ ref('high_value_currencies') }}
