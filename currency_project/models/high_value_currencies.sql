select
    currency,
    rate,
    loaded_at
from main.clean_rates
where rate > 3

