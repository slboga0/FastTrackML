
import os
import glob
import random
import string
import zipfile
import shutil
import subprocess
import pandas as pd

def add_trailing_slash(path):
    """Add a path ends with a trailing slash, regardless of the OS."""
    if not path.endswith(os.sep):  # Check for the current OS's path separator
        path += os.sep
    return path

def remove_files(file_to_remove):
    try:
        # Use subprocess to remove *.txt files in the directory
        subprocess.run(['cmd', '/c', 'del', file_to_remove], shell=True)

        print(f"*.txt files removed from {file_to_remove}")
    except Exception as e:
        print(f"Error: {e}")


def write_card_list(directory_path, output_file):
    try:
        # List files in the directory
        directories = glob.glob(os.path.join(directory_path, "*"))

        # Save the list to the specified output file
        with open(output_file, 'w') as file:
            file.write('\n'.join(directories))

        print(f"File list saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")


def remove_directory(directory_path):
    try:
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' and its contents removed successfully.")
    except Exception as e:
        print(f"Error removing directory: {e}")

def generate_horse_id(number):
    # Generate a random 3-letter prefix
    prefix = ''.join(random.choices(string.ascii_uppercase, k=3))

    # Generate a random 2-digit suffix
    suffix = ''.join(random.choices(string.digits, k=2))

    # Combine the prefix, suffix, and the provided number to create the 5-digit horse ID
    horse_id = f"{prefix}{suffix}{number:02d}"

    return horse_id




def unzip_all(zip_dir, archive_dir=None):
    """Unzips all zip files in a directory and moves them to an archive directory.

    Args:
        zip_dir: The directory containing the zip files.
        archive_dir: The directory to move the zip files to after extraction.
                     If None, a subdirectory "archive" will be created within zip_dir.
    """

    if not os.path.exists(zip_dir):
        print(f"Error: Zip directory '{zip_dir}' does not exist.")
        return

    if archive_dir is None:
        archive_dir = os.path.join(zip_dir, "archive")

    os.makedirs(archive_dir, exist_ok=True)  # Create archive directory if it doesn't exist

    for filename in os.listdir(zip_dir):
        if filename.endswith(".zip"):
            zip_path = os.path.join(zip_dir, filename)
            archive_path = os.path.join(archive_dir, filename)

            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(zip_dir)
                print(f"Unzipped '{filename}' to '{zip_dir}'.")

                # Move the zip file to the archive directory
                shutil.move(zip_path, archive_path)
                print(f"Moved '{filename}' to '{archive_dir}'.")

            except zipfile.BadZipFile:
                print(f"Error: '{filename}' is not a valid zip file.")
            except shutil.Error as e:  # Catch shutil errors (e.g., file already exists)
                print(f"Error moving '{filename}': {e}")
            except Exception as e:
                print(f"An error occurred while unzipping '{filename}': {e}")

import pandas as pd
import re

def get_field(line, idx, to_upper=False):
    """Return the stripped value at a given index; convert to upper case if needed."""
    val = line[idx].strip()
    return val.upper() if to_upper else val

def parse_records(line, start_index, field_map):
    """Parse records (e.g., past performances or workouts) based on the field map."""
    records_list = []

    for i, (field, (offset, to_upper)) in enumerate(field_map.items()):
        record = {}
        field_value = get_field(line, start_index + offset, to_upper)
        record[field] = field_value
        records_list.append(record)

    return records_list

def load_field_mapping(csv_file):
    """Load the field mapping from a CSV file."""
    mapping_df = pd.read_csv(csv_file)
    field_map = {
        row['field_number']: (int(row['position']), bool(row['to_upper']))
        for _, row in mapping_df.iterrows()
    }
    return field_map

def parse_line(line, field_mapping_csv):
    """Parse a full record dynamically reading mappings from a single CSV file."""
    record = {}

    # Load field mappings
    field_map = load_field_mapping(field_mapping_csv)

    # Parse the line based on field mappings
    for field, (idx, to_upper) in field_map.items():
        record[field] = get_field(line, idx, to_upper)

    return record


def main():
    #unzip_all(r'C:\Users\SamBo\Projects\FastTrackML\data\raw\results', r'C:\Users\SamBo\Projects\FastTrackML\data\raw\results\archive')
    #unzip_all(r'C:\Users\SamBo\Projects\FastTrackML\data\raw', r'C:\Users\SamBo\Projects\FastTrackML\data\raw\archive')

    # Define file path for field mapping
    field_mapping_csv = "fields_mapping.csv"  # CSV containing all field mappings

    # Example input line (mocked as a list of strings for demonstration)
    input_line = [""] * 1500  # Replace with actual input line split into fields.

    # Parse the line
    parsed_record = parse_line(input_line, field_mapping_csv)

    # Print the parsed record
    print(parsed_record)

if __name__ == "__main__":
    main()