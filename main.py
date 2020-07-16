
#import spotify_data
import pandas as pd

#clean spotify database
def clean_spotify_data(): 
    spotify_df= pd.read_csv("Spotify/data.csv")
    spotify_df["year"] = pd.to_numeric(spotify_df["year"])
    condition = spotify_df["year"] >= 1960
    spotify_df = spotify_df[condition]
    spotify_df["year"] = spotify_df["year"].astype(int)
    return spotify_df

spotify_df=clean_spotify_data()

# merging the 2 data sources and doing the analysis

# billboard: read, remove nulls, convert data types
billboard_df = pd.read_csv('Billboard/billboards.csv')
billboard_df.dropna(inplace=True)       #print(billboard_df.isnull().sum())

### LIMPAR OS DUPLICADOS !!!!
print(billboard_df)
billboard_df.drop_duplicates(['Top','Song_Name','Artist_Name','Date'],inplace=True)
print(billboard_df)

billboard_df['Top'] = billboard_df['Top'].astype(int)       #print(billboard_df.dtypes)

# create a table with song_name and artist_name, drop_duplicates, create a temporary_id for each song
music_artist_df = billboard_df[['Song_Name','Artist_Name']].drop_duplicates()
music_artist_df['temp_song_ID'] = range(0,len(music_artist_df))

# add the temp_song_ID to the billboard_df
billboard_df = billboard_df.merge(music_artist_df,how='left',on=['Song_Name','Artist_Name'])

# create a Popularity_score based on the positions on the top
billboard_df['Popularity_Score'] = 101-billboard_df['Top']

# create a 'Year' column
billboard_df['Year'] = billboard_df['Date'].apply(lambda dt : dt[0:4])

# group by year and song to get the popularity scores per year
yearly_scores = billboard_df.groupby(['Year','temp_song_ID','Song_Name','Artist_Name'])['Popularity_Score'].sum()



#print(yearly_scores)

# try to match song names and song_IDs