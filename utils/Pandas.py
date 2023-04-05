
import pandas as pd
import json

filter_df = lambda df, cln, val: df.loc[df[cln] == val]
pluck_row = lambda row, *clns: [row[cln].iloc[0] for cln in clns]
drop_cols = lambda df, *clns: df.drop(list(clns), axis=True, inplace=True)
num_col = lambda col: pd.to_numeric(col)
to_date = lambda col: pd.to_datetime(col, unit='ms')

unique_indexes = lambda df: df.index.unique()

unique_columns = lambda df: df.nunique()

latest_date = lambda df: str(df['date'].iloc[-1])
latest_time = lambda df: str(df.index[-1])

def set_element(df,index,cln,val):
  df.loc[index,cln] = val 
  return 


def jsonify(df: pd.DataFrame)->str:
  dict_df = df.to_dict(orient='records')
  json_dump = json.dumps(dict_df)
  return json_dump
