from src.extract import extract_apidata, get_cursor
from src.load import dump_apidata

if __name__ == "__main__":

    last_dt = get_cursor()

    extracted_tuple = extract_apidata('me/player/recently-played', last_dt)
    print(extracted_tuple)
    if extracted_tuple is not None:
        dump_apidata(extracted_tuple)
        print("Done!")

