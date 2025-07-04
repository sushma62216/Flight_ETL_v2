from transform import transformed_data
from extract import extract
from load import load_to_db
from db_schema import create_tables

def main():
    create_tables()
    df=transformed_data(extract)

    if not df.empty:
        load_to_db(df)
        print("Data loaded successfully")
    else:
        print("No data available from the API")

if __name__=="__main__":
    main()
