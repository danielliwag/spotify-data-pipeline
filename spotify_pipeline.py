from src.extract import extract_album

if __name__ == "__main__":
    df = extract_album('4aawyAB9vmqN3uQ7FjRGTy')
    print(df.columns)