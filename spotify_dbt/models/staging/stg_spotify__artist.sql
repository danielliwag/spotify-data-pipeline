{{ config(materialized='view') }}

WITH raw_data AS (
    SELECT 
        payload,
        extracted_at
    FROM {{ source ('spotify', 'stg_spotify_raw') }}
),

flattened_artist AS (
    SELECT
        item->'track'->'artists'->0->>'id' as artist_id,
        item->'track'->'artists'->0->>'name' as artist_name
    FROM
        raw_data,
        jsonb_array_elements(payload->'items') AS item
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['artist_id']) }} as artist_pk,
    artist_id,
    artist_name
FROM flattened_artist