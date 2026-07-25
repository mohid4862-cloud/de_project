select
    currency,
    round(avg(rate), 4) as avg_rate,
    round(max(rate), 4) as max_rate,
    round(min(rate), 4) as min_rate,
    count(*) as total_snapshots
from {{ ref('high_value_currencies') }}
group by currency

