{{ config(materialized='view') }}

WITH raw_data AS (
    SELECT 
        payload,
        extracted_at 
    FROM {{ source('spotify', 'stg_spotify_raw') }}
),

flattened AS (
    SELECT
        extracted_at,
        -- Use ->> for text values
        (item->>'played_at')::timestamp as played_at,
        
        -- Navigating the nested track object
        item->'track'->>'id' as track_id,
        item->'track'->>'name' as track_name,
        (item->'track'->>'duration_ms')::int as duration_ms,
        
        -- Artist info (first artist in the array)
        item->'track'->'artists'->0->>'id' as artist_id,
        item->'track'->'artists'->0->>'name' as artist_name,
        
        -- Album info
        item->'track'->'album'->>'id' as album_id,
        item->'track'->'album'->>'name' as album_name

    FROM raw_data,
         -- This function expands the 'items' array into individual rows
         jsonb_array_elements(payload->'items') AS item
)

SELECT * FROM flattened