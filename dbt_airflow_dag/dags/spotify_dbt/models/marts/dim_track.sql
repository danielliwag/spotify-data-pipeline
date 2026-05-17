{{ config(materialized='table') }}

WITH track_data AS (
    SELECT
        track_id,
        MAX(track_name) AS track_name
    FROM {{ ref('stg_spotify__recently_played') }}
    WHERE track_id IS NOT NULL
    GROUP BY track_id
)   

SELECT
    {{ dbt_utils.generate_surrogate_key(['track_id']) }} AS track_key,
    track_id,
    track_name
FROM track_data