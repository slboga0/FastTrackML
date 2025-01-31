import logging
import pandas as pd
from HorseRaceDataUtilities import generate_horse_id

def get_field(line, idx, to_upper=False):
    """Return the stripped value at a given index; remove surrounding double quotes and convert to upper case if needed."""
    try:
        val = line[idx].strip().strip('"')  # Remove surrounding double quotes
        return val.upper() if to_upper else val
    except IndexError:
        return ""  # Return an empty string if the index is out of range

def load_field_mapping_and_data(data_file, field_mapping_csv):
    """Load the field mapping and parse the data file into a DataFrame."""
    # Load field mappings
    mapping_df = pd.read_csv(field_mapping_csv)
    field_map = mapping_df[['field_name', 'predictive_feature']].to_dict(orient='records')

def map_fields_to_line(line, field_map):
    """Map a line of data to the field names using the field map."""
    line_split = line.strip().split(',')  # Assuming CSV format with commas
    record = {}
    for idx, field in enumerate(field_map):
        if idx < len(line_split):
            record[field] = get_field(line_split, idx, False)
        else:
            record[field] = ""  # Handle missing indices gracefully
    return record, field_map

def create_dataframe(data_file, field_mapping_csv):
    """Create a DataFrame from the data file using the field map."""
    # Load field mappings
    mapping_df = pd.read_csv(field_mapping_csv)
    field_map = mapping_df[['field_name', 'predictive_feature']].to_dict(orient='records')

    # Read the data file line by line and map fields
    records = []
    with open(data_file, 'r') as f:
        for line in f:
            record = map_fields_to_line(line, field_map)
            records.append(record)

    # Create a DataFrame from the parsed records
    df = pd.DataFrame(records)
    return df

def load_single_card(pp_path, field_map, x):
    """Load data for a single card and map fields."""
    all_pp_list = []
    try:
        with open(pp_path, 'r') as f:
            for counter, line in enumerate(f, start=1):
                #print (f'Counter : {x}')
                x = x + 1
                line_split = line.strip().split(',')
                record = {}
                for idx, field in enumerate(field_map):
                    if idx < len(line_split):
                        record[field['field_name']] = get_field(line_split, idx, False)
                    else:
                        record[field['field_name']] = ""
                record['horse_id'] = generate_horse_id(counter)  # Assign unique horse ID
                all_pp_list.append(record)
    except FileNotFoundError:
        logging.error(f"File not found: {pp_path}")
    except Exception as e:
        logging.error(f"An error occurred while reading {pp_path}: {e}")
    return all_pp_list, x


def load_all_pp_cards(pp_cards, field_mapping_csv):
    """Load all past performance cards into a single DataFrame."""
    logging.info('Loading PPs for all cards...')

    # Load field mappings
    mapping_df = pd.read_csv(field_mapping_csv)
    field_map = mapping_df[['field_name', 'predictive_feature']].to_dict(orient='records')

    # Accumulate parsed PP data from each card
    all_pps = []
    x = 0
    for counter, card in enumerate(pp_cards, start=1):
        filename = card.get('filename')
        if not filename:
            logging.warning(f"Skipping card {counter} with no 'filename' key.")
            continue

        logging.debug(f"Processing card {counter}: {filename}")
        single_card_pps, x = load_single_card(filename, field_map, x)
        all_pps.extend(single_card_pps)
    # Convert the aggregated list of dicts into one DataFrame
    pp_all_df = pd.DataFrame(all_pps)

    logging.info('Completed loading PPs for all cards.')
    return pp_all_df, field_map

# Example usage
if __name__ == "__main__":
    # Define file paths
    field_mapping_csv = "fields_mapping.csv"  # CSV containing all field mappings
    pp_cards = [
        {"filename": "card1.csv"},
        {"filename": "card2.csv"}
    ]

   
    # Load all PP cards into a DataFrame
    df = load_all_pp_cards(pp_cards, field_mapping_csv)

    # Print the resulting DataFrame
    print(df)
