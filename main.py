import sys
from src.app import run_app
from src.data_insertion import insert_assay_data_from_csv



def main():
    """
    Main function to run the app.
    If we do the following in the CLI:
    - python main.py run -> it runs the app by calling run_app() from app.py
    - python main.py insert data.csv -> it inserts data from data.csv to the database by calling insert_data_from_csv() from data_insertion.py
    """
    if sys.argv[1] == "run":
        run_app()
    elif sys.argv[1] == "insert":
        insert_assay_data_from_csv(sys.argv[2])
    else:
        print("Invalid command.")
        print("Please use the following commands:")
        print(f"- python main.py run")
        print(f"- python main.py insert data.csv")


if __name__ == "__main__":
    main()