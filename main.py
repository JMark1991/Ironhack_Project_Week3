
#import spotify_data
import pandas as pd

# merging the 2 data sources and doing the analysis

# billboard: read, remove nulls, convert data types
billboard_df = pd.read_csv('Billboard/billboards.csv')
billboard_df.dropna(inplace=True)       #print(billboard_df.isnull().sum())
billboard_df['Top'] = billboard_df['Top'].astype(int)       #print(billboard_df.dtypes)

music_artist_df = billboard_df[['Song_Name','Artist_Name']].drop_duplicates()
music_artist_df['temp_song_ID'] = range(0,len(music_artist_df))

billboard_df = billboard_df.merge(music_artist_df,how='left',on=['Song_Name','Artist_Name'])

billboard_df['Popularity_Score'] = 101-billboard_df['Top']

billboard_df['Year'] = billboard_df['Date'].apply(lambda dt : dt[0:4])

yearly_scores = billboard_df.groupby(['Year','temp_song_ID','Song_Name','Artist_Name'])['Popularity_Score'].sum()
#


print(yearly_scores)

# try to match song names and song_IDs