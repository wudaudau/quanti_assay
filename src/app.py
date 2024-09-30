"""
This may need major refactoring later.

This is only for the initial development phase.
I am thinking to focus on creating the database and related functions first.
This work will be done in the db_utils.py file.
"""



from src.db_utils import create_db, add_kit_item_from_file

# main function to run the app
def run_app():
    db_path = 'data/database/quanti.sqlite'
    create_db(db_path)
    print("Database has been created.")

    add_kit_item_from_file(db_path)
    print("Kit items have been added to the database.")

    print("Hi, it's the Quanti app!")

    assay_id = ask_assay_name()



# The following are the low-level functions


def ask_assay_name() -> int:
    """
    This function asks the user to select an assay name.
    If no data is available, go to add_assay_name().
    If data is available, show the list of assay names and ask the user to select one.
        if the input is not in the list, ask the user to select again.
        else, return the assay_id.
    """
    assays = ["A", "B", "C"] # None # get_assay_names_from_db() # get assay names from the database

    if not assays:
        add_assay_name()
    else:
        print("Please select an assay name:")
        for i, assay in enumerate(assays):
            print(f"{i+1}. {assay}")

        while True:
            try:
                assay_id = int(input("Enter the number of the assay name: "))
                if assay_id < 1 or assay_id > len(assays):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        return assay_id
    
def add_assay_name():
    """
    This function asks the user to add an assay name. TODO: we will add analytes as well.
    Then insert the assay name into the database.
    """
    assay_name = input("Enter the assay name: ")
    # insert_assay_name_to_db(assay_name)
    print(f"{assay_name} has been added to the database.")




if __name__ == '__main__':
    run_app()