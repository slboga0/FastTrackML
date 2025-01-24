import logging
from pathlib import Path

def get_pp_file_list(root_dir):
    """
    Recursively find all .DRF files in the given root directory.
    Returns a list of pathlib.Path objects.
    """
    files = [path for path in Path(root_dir).rglob("*.DRF") if path.is_file()]
    return files


def scan_cards(path_cards):
    """
    Scans all PP (.DRF) files in `path_cards` directory and constructs a list of
    dicts with 'card' (file name without extension) and 'filename' (full Path).
    """
    logging.info("Scanning all PP files.")

    # Construct list of PP cards
    file_list = get_pp_file_list(path_cards)

    # Print total number of .DRF files found
    print(f"Number of .DRF files found: {len(file_list)}")

    pp_list = []
    for file_path in file_list:
        filename = file_path.name  # e.g. 'ABC0112.DRF'
        pcs = filename.split(".")

        card_info = {
            "card": pcs[0],         # e.g. 'ABC0112'
            "filename": file_path,  # Full path to the .DRF file
        }
        pp_list.append(card_info)

    return pp_list
