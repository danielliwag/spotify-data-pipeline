{{ config(materialized='view') }}

WITH raw_data AS (
    SELECT 
        payload,
        extracted_at 
    FROM {{ source('spotify', 'stg_spotify_raw') }}
),

flattened_recently_played AS (
    SELECT
        extracted_at,
        (item->>'played_at')::timestamp as played_at,
        
        # dim_tracks fields
        item->'track'->>'id' as track_id,
        item->'track'->>'name' as track_name,

        (item->'track'->>'duration_ms')::int as duration_ms,

        # dim artists fields
        item->'track'->'artists'->0->>'id' as artist_id,
        item->'track'->'artists'->0->>'name' as artist_name,

        # dim albums fields
        item->'track'->'album'->>'id' as album_id,
        item->'track'->'album'->>'name' as album_name

        # dim users fields
        user_info->>'id' as user_id,
        user_info->>'display_name' as user_display_name,
        user_info->>'country' as user_country,
        user_info->>'product' as product_type

    FROM raw_data,
         jsonb_array_elements(payload->'items') AS item
)

SELECT DISTINCT ON (played_at, track_id)
    * 
 FROM
    flattened_recently_played
<<<<<<< HEAD
ORDER BY 
    played_at, track_id, extracted_at DESC;
=======
ORDER BY
    played_at, track_id, extracted_at DESC;
>>>>>>> 9628557 (modeled the dimensions and fact table)
