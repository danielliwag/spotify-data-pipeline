import psycopg2
from include.src.config import get_db_config
from include.src.logger import PipelineLogger, log_execution

logger = PipelineLogger(__name__)

@log_execution
def dump_apidata(apidata_tuple):
    db_params = get_db_config()

    query = """
    INSERT INTO daniel.stg_spotify_raw (payload, user_info, endpoint)
    VALUES (%s, %s, %s);
    """

    logger.debug(
        "Inserting data into staging table",
        endpoint=apidata_tuple[2] if len(apidata_tuple) > 2 else None
    )

    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query, apidata_tuple)
            conn.commit()

        logger.info("Successfully loaded data to staging table")

    except Exception as e:
        logger.error(f"Failed to load data: {e}", exc_info=True)
        raise