import pandas as pd
import re

def get_field(line, idx, to_upper=False):
    """Return the stripped value at a given index; convert to upper case if needed."""
    try:
        val = line[idx].strip()
        return val.upper() if to_upper else val
    except IndexError:
        return ""  # Return an empty string if the index is out of range

def parse_records(line, start_index, field_map):
    """Parse records (e.g., past performances or workouts) based on the field map."""
    records_list = []

    for i, (field, offset) in enumerate(field_map.items()):
        field_value = get_field(line, start_index + offset, False)
        records_list.append({field: field_value})

    return records_list

def load_field_mapping(csv_file):
    """Load the field mapping from a CSV file."""
    mapping_df = pd.read_csv(csv_file)
    field_map = mapping_df[['field_name', 'predictive_feature']].to_dict(orient='records')
    return field_map

def load_field_mapping_old_deleteME(csv_file):
    """Load the field mapping from a CSV file."""
    mapping_df = pd.read_csv(csv_file)
    field_map = {
        row['field_name']: int(row['field_position'])
        for _, row in mapping_df.iterrows()
    }
    return field_map

def parse_line(line, field_map):
    """Parse a single line using the field map."""
    line_split = line.strip().split(',')  # Assuming CSV format with commas
    record = {}
    for idx, field in enumerate(field_map):
        if idx < len(line_split):
            record[field] = get_field(line_split, idx, False)
        else:
            record[field] = ""  # Handle missing indices gracefully
    return record

def parse_line_old(line, field_mapping_csv):
    """Parse a full record dynamically reading mappings from a single CSV file."""
    record = {}

    # Load field mappings
    field_map = load_field_mapping(field_mapping_csv)

    # Parse the line based on field mappings
    for field, idx in field_map.items():
        record[field] = get_field(line, idx, False)

    return record

# Example usage
if __name__ == "__main__":
    # Define file path for field mapping
    field_mapping_csv = "File_Format_Description.csv"  # CSV containing all field mappings

    # Example input line (mocked as a list of strings for demonstration)
    input_line = [""] * 1500  # Replace with actual input line split into fields.

    # Parse the line
    parsed_record = parse_line(input_line, field_mapping_csv)

    # Print the parsed record
    print(parsed_record)
