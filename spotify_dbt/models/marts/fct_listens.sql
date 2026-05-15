{{ config(materialized='table') }}

WITH listens_data AS (
    SELECT
        track_id,
        artist_id,
        album_id,
        user_id,
        played_at,
        duration_ms
    FROM {{ ref('stg_spotify__recently_played') }}
)

SELECT
    {{ dbt_utils.surrogate_key(['user_id', 'track_id', 'played_at']) }} AS listen_key,
    {{ dbt_utils.surrogate_key(['user_id']) }} AS user_key,
    {{ dbt_utils.surrogate_key(['track_id']) }} AS track_key,
    {{ dbt_utils.surrogate_key(['artist_id']) }} AS artist_key,
    {{ dbt_utils.surrogate_key(['album_id']) }} AS album_key,
    played_at,
    duration_ms
FROM listens_data;