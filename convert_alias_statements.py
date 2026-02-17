import os
import json
import pandas as pd


alias_data_dir = './alias_statements'
alias_csv_dir = './alias_csvs'


dfs = []
for filename in os.listdir(alias_data_dir):                            # For all files in the alias statement directory:
  if filename.endswith(".json"):                                       #     If file is .json format, then:
    file_path = os.path.join(alias_data_dir, filename)                 #        Build the full file path string

    with open(file_path, 'r') as f:                                    #        Open file at file_path:
        file_num = "".join(char for char in filename if char.isdigit())
        data_as_dict = json.load(f)                                            #            Load json content into a dict (hint: json.load() is very useful here)
        df = pd.DataFrame(data_as_dict['suspect_statement'])
        df['name'] = data_as_dict['name']
        df['file_num'] = file_num
        dfs.append(df)

alias_statements_df = pd.concat(dfs, ignore_index=True)

os.makedirs(alias_csv_dir, exist_ok=True)
alias_statements_df.to_csv(os.path.join(alias_csv_dir, 'all_alias_statements.csv'), index=False)
print(f"Saved `all_alias_statements.csv` to {alias_csv_dir}")
