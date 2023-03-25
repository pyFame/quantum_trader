import pandas as pd

pluck = lambda dict, *args: (dict[arg] for arg in args)
filter_df = lambda df, cln, val: df.loc[df[cln] == val]
pluck_row = lambda row, *clns: [row[cln].iloc[0] for cln in clns]
drop_cols = lambda df, *clns: df.drop(list(clns), axis=True, inplace=True)
num_col = lambda col: pd.to_numeric(col)
to_date = lambda col: pd.to_datetime(col, unit='ms')