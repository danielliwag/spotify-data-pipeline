{{ config(materialized='table') }}

WITH album_data AS (
    SELECT
        album_id,
        MAX(album_name) AS album_name
    FROM {{ ref('stg_spotify__recently_played') }}
    WHERE album_id IS NOT NULL
    GROUP BY album_id
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['album_id']) }} AS album_key,
    album_id,
    album_name
FROM album_data