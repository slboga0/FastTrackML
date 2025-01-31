import re
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime
from HorseRaceDataFindPPs import scan_cards
from HorseRaceDataReader import load_all_pp_cards
from HorseRaceDataResultReader import load_all_result

def load_data(params, vrsn_name, track="*.DRF", saveFeatureDataToFile=False):
    """
    Generate features by merging Past-Performance (PP) data with race results.
    """
    # ----------------------------------------------------------------------
    # 1. Load Past Performance data
    # ----------------------------------------------------------------------
    logging.info("Scanning past performance cards.")
    pp_cards = scan_cards(params.past_perf_data, track)

    #print (f'pp_cards = {pp_cards}')
    pp_all_df,field_map = load_all_pp_cards(pp_cards, params.field_mapping_csv)

    # Group by date and display counts
    grouped_counts = pp_all_df.groupby("date")["date"].count()
    logging.info("Grouped counts by date:")
    logging.info(grouped_counts.head())
    logging.info(grouped_counts.tail())

    # ----------------------------------------------------------------------
    # 2. Load the race results
    # ----------------------------------------------------------------------
    logging.info("Loading race results.")
    res_dict, keys = load_all_result(params.results_file_dir)
    result = pd.DataFrame(res_dict, columns=keys)

    # Rename result columns to avoid clashes with PP column names
    result.columns = ['res_' + c for c in keys]

    # Clean up horse names in results
    result['cln_name'] = (
        result['res_name']
        .str.replace(r'\((.+)\)', '', regex=True)
        .str.rstrip()
    )

    # ----------------------------------------------------------------------
    # 3. Create a unique key for merging
    # ----------------------------------------------------------------------
    logging.info("Creating unique keys for merging.")
    pp_all_df['race_key'] = (
        pp_all_df['track'].astype(str) + '_' +
        pp_all_df['date'].astype(str) + '_' +
        pp_all_df['race_no'].astype(str) + '_' +
        pp_all_df['entry'].astype(str)
    )

    result['race_key'] = (
        result['res_track'].astype(str) + '_' +
        result['res_date'].astype(str) + '_' +
        result['res_race_num'].astype(str) + '_' +
        result['cln_name'].astype(str)
    )

    # ----------------------------------------------------------------------
    # 4. Merge PP data with results
    # ----------------------------------------------------------------------
    logging.info("Merging past performance data with results.")
    merged_df = pd.merge(
        pp_all_df,
        result,
        how='left',
        on='race_key',
        suffixes=('', '_dup')
    )

    # Drop duplicate entries if any
    merged_df.drop_duplicates(subset=['race_key'], keep='first', inplace=True)

    # ----------------------------------------------------------------------
    # 5. Save the merged data to file if required
    # ----------------------------------------------------------------------
    if saveFeatureDataToFile:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_dir = Path(params.output_feature_dir, vrsn_name)
        output_dir.mkdir(parents=True, exist_ok=True)

        features_csv_filename = output_dir / f"features_{timestamp}.csv"
        merged_df.to_csv(features_csv_filename, index=False)

        logging.info(f"Features saved to {features_csv_filename}")

    # ----------------------------------------------------------------------
    # 6. Return the final merged DataFrame
    # ----------------------------------------------------------------------
    return merged_df,field_map

# Example usage
if __name__ == "__main__":
    class MockParams:
        past_perf_data = "path/to/pp_data"
        results_file_dir = "path/to/results"
        field_mapping_csv = "fields_mapping.csv"
        output_feature_dir = "path/to/output"

    params = MockParams()
    version_name = "v1.0"
    track = "SA*.DRF"

    # Generate features
    df = load_data(params, version_name, track, saveFeatureDataToFile=True)
    print(df.head())