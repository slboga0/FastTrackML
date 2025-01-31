import os
import logging
from pathlib import Path

from HorseRaceDataUtilities import add_trailing_slash

# Enable debugging level
logging.basicConfig(level=logging.INFO) 
logFormatter = logging.Formatter(fmt=' %(name)s :: %(levelname)-8s :: %(message)s')

# Define directories for this program (relative to the parent folder Horese_Race_Handicapper)
current_working_directory = os.getcwd()
#logging.debug('Current working directory = {}', current_working_directory)

# Data folder for input and output files
data_dir = add_trailing_slash(os.path.join(current_working_directory, "Data"))
#logging.debug("Data Directory = ", data_dir)

input_data_dir = add_trailing_slash(os.path.join(data_dir, "raw"))
#logging.debug("Input Files Directory = ", input_data_dir)

input_data_dir_todays_race = add_trailing_slash(os.path.join(data_dir, "raw"))
#logging.debug("Input Files Directory = ", input_data_dir)

bris_data_dir = add_trailing_slash(os.path.join(input_data_dir, "Brisnet"))
#logging.debug("Bris Data Directory = ", bris_data_dir)

past_perf_data = add_trailing_slash(os.path.join(data_dir, "raw"))
#logging.debug("Past Performance File Directory = ", past_perf_data)

results_file_dir = add_trailing_slash(os.path.join(data_dir, "raw\\results"))
#logging.debug("Result File Directory = ", results_file_dir)

# Working and Output data will be store in the following locations
output_directory = add_trailing_slash(os.path.join(data_dir, "predictions"))
#logging.debug("Output Directory = ", output_directory)

log_directory = add_trailing_slash(os.path.join(current_working_directory, "Log"))
#logging.debug("Output Directory = ", log_directory)

temp_directory = add_trailing_slash(os.path.join(current_working_directory, "Temp"))
#logging.debug("Temp Working Directory = ", temp_path)

output_feature_dir = add_trailing_slash(os.path.join(output_directory, "Features"))
#logging.debug("Output features Directory = ", temp_path)

field_mapping_csv = "fields_mapping.csv"

# Feature processing parameters
max_npp = 10
max_nwrk = 12
