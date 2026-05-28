from include.src.extract import extract_apidata, get_cursor
from include.src.load import dump_apidata



def run_pipeline():
    cursor = get_cursor()

    extracted_tuple = extract_apidata('me/player/recently-played', cursor)
    
    if extracted_tuple is None:
        print("No new data to load. Exiting.")

    else:
        dump_apidata(extracted_tuple)
    print("Done!")