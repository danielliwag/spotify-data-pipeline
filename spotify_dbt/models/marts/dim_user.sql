{{ config(materialized='table') }}

WITH user_data AS (
    SELECT
        user_id,
        MAX(user_display_name) AS user_display_name,
        MAX(user_country) AS user_country,
        MAX(product_type) AS product_type
    FROM {{ ref('stg_spotify__recently_played') }}
    WHERE user_id IS NOT NULL
    GROUP BY user_id
)   

SELECT
    {{ dbt_utils.generate_surrogate_key(['user_id']) }} AS user_key,
    user_id,
    user_display_name,
    user_country,
    product_type
FROM user_data