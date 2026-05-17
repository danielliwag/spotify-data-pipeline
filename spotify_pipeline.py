from src.extract import extract_apidata, get_cursor, get_user
from src.load import dump_apidata

if __name__ == "__main__":


    def run_pipeline():
        cursor = get_cursor()

        extracted_tuple = extract_apidata('me/player/recently-played', cursor)
    
        if extracted_tuple is None:
            print("No new data to load. Exiting.")

        else:
            dump_apidata(extracted_tuple)
            print("Done!")

    run_pipeline()