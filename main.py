
#import spotify_data
import pandas as pd

# merging the 2 data sources and doing the analysis

# billboard
billboard_df = pd.read_csv('Billboard/billboards.csv')

print(billboard_df.dtypes)