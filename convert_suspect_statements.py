import os
import json
import pandas as pd

# objective: convert 6 suspect statements into 3 files:
# suspect_statements.csv: (name, time, location, activity)
# gps_activity.csv: (name, time, location, signal_strength)
# witness_data.csv: (suspect_name, witness_name, witness_reliability, time, loc, act)
# getting there:
# I'll create dictionary for each, where keys are the column names
# and their values are a column of data (eg, a column of times)
# I'll wrap each dictionary in a pandas dataframe 
# then save each as a csv

# a pd DataFrame takes in a dictionary where the col names are keys and 
# the column values are lists

def make_suspect_statements_dict(jsons):
    all_sus_states = {'name':[], 'time':[], 'location':[], 'activity':[]}
    for file_name in jsons:
        with open(file_name, 'r') as fp:
            cur_raw_data = json.load(fp)
            cur_suspect_name = cur_raw_data['name']
            cur_suspect_statement = cur_raw_data['suspect_statement']
            # cur_suspect_statement is a list of (time, location, act) dicts
            for tla_dict in cur_suspect_statement:
                all_sus_states['name'].append(cur_suspect_name)
                all_sus_states['time'].append(tla_dict['time'])
                all_sus_states['location'].append(tla_dict['location'])
                all_sus_states['activity'].append(tla_dict['activity'])

    return all_sus_states

def make_suspect_statements_csv(jsons, csv_dir):
    dict_for_pd = make_suspect_statements_dict(jsons)
    sus_state_df = pd.DataFrame(dict_for_pd)
    csv_path = f'{csv_dir}/suspect_statements.csv'
    os.makedirs(csv_dir, exist_ok=True)
    sus_state_df.to_csv(csv_path, index=False)
    print(f'suspect statements csv generated & saved to {csv_path}')


def make_gps_activity_dict(jsons):
    all_gps_data = {'name':[], 'time':[], 'location':[], 'signal_strength':[]}
    for file_name in jsons:
        with open(file_name, 'r') as fp:
            cur_raw_data = json.load(fp)
            cur_suspect_name = cur_raw_data['name']
            cur_gps_data = cur_raw_data['gps_data']
            # cur_suspect_statement is a list of (time, location, act) dicts
            for tls_dict in cur_gps_data:
                all_gps_data['name'].append(cur_suspect_name)
                all_gps_data['time'].append(tls_dict['time'])
                all_gps_data['location'].append(tls_dict['location'])
                all_gps_data['signal_strength'].append(tls_dict['signal_strength'])

    return all_gps_data

def make_gps_csv(jsons, csv_dir):
    dict_for_pd = make_gps_activity_dict(jsons)
    sus_state_df = pd.DataFrame(dict_for_pd)
    csv_path = f'{csv_dir}/gps_activity.csv'
    os.makedirs(csv_dir, exist_ok=True)
    sus_state_df.to_csv(csv_path, index=False)
    print(f'gps data csv generated & saved to {csv_path}')

def make_witness_dict(jsons):
    all_witness_data = {'suspect_name':[], 'witness_name':[], 'witness_reliability':[], 'time':[], 'location':[], 'activity':[]}
    for file_name in jsons:
        with open(file_name, 'r') as fp:
            cur_raw_data = json.load(fp)
            cur_suspect_name = cur_raw_data['name']
            # gonna need an outer loop over witness name
            for cur_witness_name, cur_witness_dict in cur_raw_data['witness_statements'].items():
                cur_witness_reliability = cur_witness_dict['witness_reliability']
                # cur_suspect_statement is a list of (time, location, act) dicts
                for tla_dict in cur_witness_dict['observations']:
                    all_witness_data['suspect_name'].append(cur_suspect_name)
                    all_witness_data['witness_name'].append(cur_witness_name)
                    all_witness_data['witness_reliability'].append(cur_witness_reliability)
                    all_witness_data['time'].append(tla_dict['time'])
                    all_witness_data['location'].append(tla_dict['location'])
                    all_witness_data['activity'].append(tla_dict['activity'])

    return all_witness_data

def make_witness_data_csv(jsons, csv_dir):
    dict_for_pd = make_witness_dict(jsons)
    sus_state_df = pd.DataFrame(dict_for_pd)
    csv_path = f'{csv_dir}/witness_data.csv'
    os.makedirs(csv_dir, exist_ok=True)
    sus_state_df.to_csv(csv_path, index=False)
    print(f'witness data csv generated & saved to {csv_path}')

def main():
    csv_dir ='./suspect_csvs'
    suspect_data_dir = './suspect_statements'
    print(f"This program expects suspect statement json files to be in {suspect_data_dir}. It will save csvs to {csv_dir}")
    jsons = [os.path.join(suspect_data_dir, f) for f in os.listdir(suspect_data_dir) if f.endswith('.json')]
    make_suspect_statements_csv(jsons, csv_dir)
    make_gps_csv(jsons, csv_dir)
    make_witness_data_csv(jsons, csv_dir)

if __name__ == '__main__':
    main()

