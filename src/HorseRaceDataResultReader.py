import csv
from pathlib import Path

def get_result_file_list(root_dir):
    files = []
    for path in Path(root_dir).rglob("*.*"):
        if path.is_file():
            files.append(path)
    return files

def load_all_result(results_file_dir):

    surf_dict = dict()
    surfcnd_dict = dict()
    weather_dict = dict()
    temp_dict = dict()
    wps_pool_dict = dict()
    runup_dict = dict()
    all_results = []
    result = dict()

    result_file_list = get_result_file_list(results_file_dir)

    for cline in result_file_list:
        file_ext = cline.name.split(".")[-1]
        if file_ext == '1':
            parse_result_1(cline, runup_dict, surf_dict, surfcnd_dict, temp_dict, weather_dict, wps_pool_dict)
        elif file_ext == '2':
            result = parse_result_2(all_results, cline, runup_dict, surf_dict, surfcnd_dict, temp_dict,
                                    weather_dict, wps_pool_dict)

    return all_results, result.keys()

def parse_result_2(all_results, cline, runup_dict, surf_dict, surfcnd_dict, temp_dict, weather_dict, wps_pool_dict):
    with open(cline, 'r') as fh:
        reader = csv.reader(fh)
        ## Each line of the results is a horse in a race
        for line in reader:
            ## Parse the horse's data (this function grabs all the data available)
            result = parse_result_line(line)
            
            ## Add in race-level data from prior result read
            result['surf'] = surf_dict[result['race_num']]
            result['surfcnd'] = surfcnd_dict[result['race_num']]
            result['weather'] = weather_dict[result['race_num']]
            result['temp'] = temp_dict[result['race_num']]
            result['wps_pool'] = wps_pool_dict[result['race_num']]
            result['runup'] = runup_dict[result['race_num']]

            all_results.append(result)
    return result

def parse_result_line(line):
    res = dict()
    res['track'] = line[0].strip().upper()
    res['date'] = line[1].strip()
    res['race_num'] = int(line[2].strip())
    res['name'] = line[4].strip().upper()
    res['post'] = int(line[7].strip())
    res['ptodds'] = float(line[30].strip())
    res['finish'] = int(line[59].strip())
    res['btn_lengths'] = float(line[72].strip()) # Winner = 0.0

    tmp = line[50]
    if tmp != '':
        res['win_pay'] = float(tmp.strip())
    else:
        res['win_pay'] = 0.0

    tmp = line[51]
    if tmp != '':
        res['plc_pay'] = float(tmp.strip())
    else:
        res['plc_pay'] = 0.0

    tmp = line[52]
    if tmp != '':
        res['shw_pay'] = float(tmp.strip())
    else:
        res['shw_pay'] = 0.0
    return res

def parse_result_1(cline, runup_dict, surf_dict, surfcnd_dict, temp_dict, weather_dict, wps_pool_dict):
    with open(cline, 'r') as fh:
        reader = csv.reader(fh)
        for line in reader:
            race_num = int(line[2].strip())
            surf = line[8].strip()  # includes new (A) for all-weather indicator
            surf_cnd = line[37].strip()
            weather = line[62].strip()
            temp = line[63].strip()
            wps_pool = line[64].strip()
            runup = line[65].strip()  # no units specified (feet?)

            surf_dict[race_num] = surf
            surfcnd_dict[race_num] = surf_cnd
            weather_dict[race_num] = weather
            temp_dict[race_num] = temp
            wps_pool_dict[race_num] = wps_pool
            runup_dict[race_num] = runup
