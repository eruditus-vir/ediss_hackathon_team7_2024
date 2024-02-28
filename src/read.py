import pandas as pd

def load_data_xlsx(file_path):
    return pd.read_excel(file_path)

def read_and_print_file(file_path):
    """
    Reads a file from the given path and prints its contents.

    Parameters:
    file_path (str): The path to the file to be read.
    """
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            print(contents)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except IOError:
        print(f"Error reading file: {file_path}")


