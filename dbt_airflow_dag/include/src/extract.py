import psycopg2
from psycopg2.extras import Json
from include.src.config import get_access, get_db_config
from include.src.logger import PipelineLogger, log_execution

logger = PipelineLogger(__name__)


@log_execution
def get_user():
    sp = get_access()

    try:
        user_info = sp.me()
        logger.debug("Retrieved user info", user_id=user_info.get("id"))
        return user_info

    except Exception as e:
        logger.error(f"Failed to get user info: {e}", exc_info=True)
        raise


@log_execution
def extract_apidata(endpoint, cursor):

    sp = get_access()
    logger.info("Starting data extraction", endpoint=endpoint, has_cursor=cursor is not None)

    try:
        raw_data = sp.current_user_recently_played(limit=50, after=cursor)
        user_info = get_user()

        if not raw_data or not raw_data.get('items'):
            logger.info("No new data to extract since last execution", endpoint=endpoint)
            return None

        if not user_info:
            logger.warning("Failed to retrieve user information", endpoint=endpoint)
            return {}

        items_count = len(raw_data.get('items', []))
        logger.info(
            "Successfully extracted data",
            endpoint=endpoint,
            items_count=items_count,
            user_id=user_info.get('id')
        )

        return Json(raw_data), Json(user_info), endpoint

    except Exception as e:
        logger.error(f"Extraction failed: {e}", exc_info=True, endpoint=endpoint)
        raise


@log_execution
def get_cursor():
    db_params = get_db_config()

    query = """
    SELECT payload->'cursors'->>'after'
    FROM daniel.stg_spotify_raw
    WHERE payload->'cursors'->>'after' IS NOT NULL
    ORDER BY extracted_at DESC
    LIMIT 1;
    """

    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchone()

                if result and result[0]:
                    logger.debug("Retrieved cursor from database", cursor=result[0])
                    return result[0]

                logger.info("No cursor found in database, will fetch from beginning")
                return None

    except Exception as e:
        logger.error(f"Failed to retrieve cursor: {e}", exc_info=True)
        raise