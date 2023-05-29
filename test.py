from dga.plotlydash.data import create_dataframe
import pandas as pd

df = create_dataframe()

if isinstance(df, pd.DataFrame):
    print(f"df is a Pandas DataFrame: {df}")
