{{ config(materialized='view') }}

WITH raw_data AS (
    SELECT 
        payload,
        extracted_at,
        user_info
    FROM {{ source('spotify', 'stg_spotify_raw') }}
),

flattened_recently_played AS (
    SELECT
        extracted_at,
        (item->>'played_at')::timestamp AS played_at,

        -- dim_tracks fields
        item->'track'->>'id' AS track_id,
        item->'track'->>'name' AS track_name,

        (item->'track'->>'duration_ms')::int AS duration_ms,

        -- dim artists fields
        item->'track'->'artists'->0->>'id' AS artist_id,
        item->'track'->'artists'->0->>'name' AS artist_name,

        -- dim albums fields
        item->'track'->'album'->>'id' AS album_id,
        item->'track'->'album'->>'name' AS album_name,

        -- dim users fields
        user_info->>'id' AS user_id,
        user_info->>'display_name' AS user_display_name,
        user_info->>'country' AS user_country,
        user_info->>'product' AS product_type

    FROM raw_data,
         jsonb_array_elements(payload->'items') AS item
)

SELECT DISTINCT ON (played_at, track_id)
    * 
 FROM
    flattened_recently_played
ORDER BY
    played_at, track_id, extracted_at DESC
