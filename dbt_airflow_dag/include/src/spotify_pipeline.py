from include.src.extract import extract_apidata, get_cursor
from include.src.load import dump_apidata
from include.src.logger import PipelineLogger

logger = PipelineLogger(__name__)


def run_pipeline():
    logger.start_operation("spotify_etl_pipeline")

    cursor = get_cursor()

    extracted_tuple = extract_apidata('me/player/recently-played', cursor)

    if extracted_tuple is None:
        logger.info("No new data to load. Exiting pipeline early.")
        logger.end_operation("spotify_etl_pipeline", success=True, records_loaded=0)
        return

    dump_apidata(extracted_tuple)
    logger.end_operation("spotify_etl_pipeline", success=True, records_loaded=1)
    logger.info("Pipeline completed successfully")