import configparser
import datetime, argparse
import logging, os, shutil
from datetime import datetime

from HorseRaceDataIngest import load_data
from HorseRaceDataUtilities import add_trailing_slash
import HorseRaceParams

def processor_setup():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='The program constructs a *.csv file from all historical data available in /inputs/<version>/')
    parser.add_argument('-v', '--version', help='Dataset version name.', default='vrsn-NONE')
    args = parser.parse_args()

    # Create output directory (if necessary)
    out_path = HorseRaceParams.output_directory
    if not os.path.isdir(out_path):
        print('Creating ' + out_path)
        os.makedirs(out_path)

    # Create log directory (if necessary)
    out_path = HorseRaceParams.log_directory
    if not os.path.isdir(out_path):
        print('Creating ' + out_path)
        os.makedirs(out_path)

    # Create tmp directory (if necessary)
    out_path = HorseRaceParams.temp_directory
    if not os.path.isdir(out_path):
        print('Creating ' + out_path)
        os.makedirs(out_path)

    # Set-up logging (now that output and log is available)
    current_time = datetime.now().strftime("%Y_%b_%d_%H_%M_%S")
    log_filename = HorseRaceParams.log_directory + f"run_bristools_{current_time}_log.txt"

    # Modify the log filename to replace invalid characters
    log_filename = log_filename.replace(":", "_").replace(" ", "_")

    configure_logging(log_filename)

    # Create features directory (if necessary)
    out_path = HorseRaceParams.output_feature_dir
    if not os.path.isdir(out_path):
        logging.info('Creating ' + out_path)
        os.makedirs(out_path)

    # Create new dataset version directory (delete previous if necessary)
    out_path = add_trailing_slash(os.path.join(HorseRaceParams.output_feature_dir, args.version))
    if not os.path.isdir(out_path):
        logging.info('Path ' + out_path + ' not found')
        logging.info('Creating ' + out_path)
        os.makedirs(out_path)

    return args.version

def configure_logging(log_file):
    try:
        # Make sure the directory for the log file exists
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)

        # Configure logging
        logging.basicConfig(filename=log_file, level=logging.INFO)
        logging.info("Logging started.")
    except Exception as e:
        print(f"Error configuring logging: {e}")


def remove_directory(directory_path):
    try:
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' and its contents removed successfully.")
    except Exception as e:
        print(f"Error removing directory: {e}")

def run_data_prep(track):
    version_num = processor_setup()

    data_frame, field_map = load_data(HorseRaceParams, version_num, track)

    return data_frame, field_map

if __name__ == '__main__':

    #script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_dir = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", ".."))
    config_file_path = os.path.join(script_dir, '..', 'config.ini')

    print(f"Script directory: {script_dir}")  # Print the script's directory
    print(f"Config file path: {config_file_path}")  # Print the constructed path

    # Check if the file exists:
    if os.path.exists(config_file_path):
        print("Config file exists!")
    else:
        print("Config file DOES NOT EXIST at the specified path!")

    config = configparser.ConfigParser()
    config.read(config_file_path)

    track = config["DEFAULT"].get("track", "SA")

    run_data_prep(track)
