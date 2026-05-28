select
    played_at
from
    {{ ref('fct_listens') }}
where
    played_at < '2026-05-01'::date