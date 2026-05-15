{{ config(materialized='table') }}

WITH artist_data AS (
    SELECT
        artist_id,
        MAX(artist_name) as artist_name
    FROM {{ ref('stg_spotify__recently_played') }}
    WHERE artist_id IS NOT NULL
    GROUP BY artist_id
)   

SELECT
    {{ dbt_utils.surrogate_key(['artist_id']) }} AS artist_key,
    artist_id,
    artist_name
FROM artist_data;