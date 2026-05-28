-- This test will look for any negative value.

select
    duration_ms
from
    {{ ref('fct_listens') }}
where duration_ms < 0