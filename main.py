
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker


def clean_spotify_data(): 
    # read the spotify_database
    # clean the data
    # output: clean_database
    spotify_df= pd.read_csv("Spotify/data.csv")
    spotify_df["year"] = pd.to_numeric(spotify_df["year"])
    condition = spotify_df["year"] >= 1960
    spotify_df = spotify_df[condition]
    spotify_df["year"] = spotify_df["year"].astype(int)
    spotify_df.drop_duplicates(['name','artists'],inplace=True)
    return spotify_df


def find_spotify_id(music_artist_df,spotify_df):
    # input: music_artist_df, spotify_df
    # Find the spotify_id of the songs
    # output: updated music_artist_df


    # split the artists by: "&"" and "feat"
    rules = '\s*&\s*|\s+[Ff]eat\w*\s+'
    music_artist_df['Primary_Artist'] = music_artist_df['Artist_Name'].apply(lambda art : re.split(rules,art)[0])
    music_artist_df['Artists_List'] = music_artist_df['Artist_Name'].str.split(rules)


    # Match song names not duplicated
    remove_song_dup_df = music_artist_df.drop_duplicates(['Song_Name'])
    remove_song_dup_df = remove_song_dup_df.merge(spotify_df[['name','id']], how='inner', left_on='Song_Name', right_on='name')
    music_artist_df = music_artist_df.merge(remove_song_dup_df[['temp_song_ID','id']], how='left', on= 'temp_song_ID')


    # Match the song and the first artist
    temp_spot_df = spotify_df[['name', 'artists','id']]
    temp_spot_df['primary_artist'] = temp_spot_df['artists'].apply(lambda art : re.split("\'\,",art)[0].replace("['","").replace("']",""))

    temp_music_artist_df = music_artist_df[music_artist_df['id'].isnull()]
    temp_music_artist_df.drop('id', axis=1, inplace=True)
    temp_music_artist_df = temp_music_artist_df.merge(temp_spot_df, how='inner', left_on=['Song_Name','Primary_Artist'], right_on=['name','primary_artist'])

    music_artist_df = music_artist_df.append(temp_music_artist_df[['Song_Name', 'Artist_Name', 'temp_song_ID', 'Primary_Artist','Artists_List', 'id']])
    music_artist_df.drop_duplicates('temp_song_ID',keep='last',inplace=True)
    
    # Remove the remaining spotify_id NaNs 
    music_artist_df = music_artist_df[music_artist_df['id'].notna()]
    
    #print('music_artist_df: \n',music_artist_df)
    
    return music_artist_df, temp_spot_df
    


# read and clean spotify data
spotify_df = clean_spotify_data()


# billboard: read, remove nulls, drop duplication, convert data types
billboard_df = pd.read_csv('Billboard/billboards.csv')
billboard_df.dropna(inplace=True)       #print(billboard_df.isnull().sum())
billboard_df.drop_duplicates(['Top','Song_Name','Artist_Name','Date'],inplace=True)
billboard_df['Top'] = billboard_df['Top'].astype(int)       #print(billboard_df.dtypes)


# create a table with song_name and artist_name, drop_duplicates, create a temporary_id for each song
music_artist_df = billboard_df[['Song_Name','Artist_Name']].drop_duplicates()
music_artist_df['temp_song_ID'] = range(0,len(music_artist_df))


# add the temp_song_ID to the billboard_df
billboard_df = billboard_df.merge(music_artist_df,how='left',on=['Song_Name','Artist_Name'])

# Update the music_artist_df with the spotify song ids
music_artist_df, spotify_artist_df = find_spotify_id(music_artist_df,spotify_df)


# create a Popularity_score based on the positions on the top
billboard_df['Popularity_Score'] = 101-billboard_df['Top']

# create a 'Year' and 'Decade' columns
billboard_df['Year'] = billboard_df['Date'].apply(lambda dt : dt[0:4])
billboard_df['Decade'] = billboard_df['Date'].apply(lambda dt : dt[0:3] + '0')


#print column names
#print("\nbillboard:\n",billboard_df.columns,"\nmusic_artist:\n",music_artist_df.columns,"\nspotify:\n",spotify_df.columns)


# Merge dataframes
ultimate_df = music_artist_df[['id','Song_Name','Primary_Artist', 'temp_song_ID']]
ultimate_df = ultimate_df.merge(billboard_df[['temp_song_ID','Date','Year','Decade','Popularity_Score']], how='left',on='temp_song_ID')
ultimate_df = ultimate_df.merge(spotify_df[['id', 'acousticness', 'danceability', 'energy', 'explicit', 'instrumentalness', 'liveness', 'loudness',
                                            'popularity', 'speechiness', 'tempo', 'valence']], how='left', on='id')

ultimate_df['acousticness'] = pd.to_numeric(ultimate_df['acousticness']).astype(float)


def wavg(group, avg_name, weight_name):
    """ http://stackoverflow.com/questions/10951341/pandas-dataframe-aggregate-function-using-multiple-columns
    In rare instance, we may not have weights, so just return the mean. Customize this if your business case
    should return otherwise.
    """
    d = group[avg_name]
    w = group[weight_name]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return d.mean()


ultimate_df['Primary_Artist'].value_counts().head(1000).to_csv('artist_tops.csv')
# Weighted averages per year of the variables: missing 'acousticness', 
weighted_avg = pd.DataFrame()
top_artists = pd.DataFrame()
#max_val = pd.DataFrame()
#min_val = pd.DataFrame()
important_variables = ['acousticness','danceability', 'energy', 'valence', 'explicit']
#variables = ['acousticness','danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'popularity', 'speechiness', 'tempo', 'valence','explicit']
for variable in important_variables:
    weighted_avg[variable] = ultimate_df.groupby('Year').apply(wavg, variable, 'Popularity_Score')
    top_artists[variable] = ultimate_df.groupby(['Decade','Primary_Artist']).apply(wavg, variable, 'Popularity_Score')
    #max_val[variable] = ultimate_df.groupby('Decade')[variable].max()
    #min_val[variable] = ultimate_df.groupby('Decade')[variable].min()

weighted_avg.index = weighted_avg.index.astype(int)
#print(top_artists.sort_values(['explicit'], ascending=False).head(50))

'''
# line plot of the variables
sns.set_style('darkgrid')
f = plt.figure(figsize=(20,20))
ax = sns.lineplot(data=weighted_avg)
plt.rcParams['axes.grid'] = True
plt.rcParams['savefig.transparent'] = True

plt.show()
'''

'''
# pair plot of the variables
ax = sns.pairplot(data=weighted_avg)
plt.show()
'''


# group by year and song to get the popularity scores per year
yearly_scores = billboard_df.groupby(['Year','temp_song_ID','Song_Name','Artist_Name'])['Popularity_Score'].sum()
decade_scores = billboard_df.groupby(['Decade','temp_song_ID','Song_Name','Artist_Name'])['Popularity_Score'].sum()

#print(yearly_scores.sort_values(ascending=False).head(20))
#decade_tops = billboard_df.groupby(['Decade','temp_song_ID','Song_Name','Artist_Name']).apply(lambda x: x.nlargest(5,['Popularity_Score'])).reset_index(drop=True)




#answer question : whats the artist efficiency?
#Make series with primary artist and count of songs in billboard and spotify, respectively
count_songs_bill = music_artist_df.groupby(['Primary_Artist'])['Song_Name'].count()
count_songs_spoty = spotify_artist_df.groupby(['primary_artist'])['name'].count()

#create a new DataFrame 
answer_df = pd.DataFrame(count_songs_bill)
#add the second series as a column
answer_df['count_spot']= count_songs_spoty
#Drop the nulls
answer_df.dropna(inplace=True)  
#rename columns
answer_df = answer_df.rename(columns={"Song_Name": "Number of Songs on Billboard", "count_spot": "Number of Songs on Spotify"})
#add new column with the division of the other two columns
answer_df['Artist Efficiency']= answer_df['Number of Songs on Billboard']/answer_df['Number of Songs on Spotify']

#apply conditions so that the artist efficiency is not more than 1 and the minimun number of songs on spotify is 10
condition = answer_df['Artist Efficiency'] < 1
answer_df = answer_df[condition]
condition2= answer_df['Number of Songs on Spotify'] >= 10
answer_dff= answer_df[condition2]

#make a scatter plot with answer_dff
sns.set_style('darkgrid')

f = plt.figure(figsize=(20,20))
graph_eff = sns.scatterplot(x="Number of Songs on Spotify",y="Number of Songs on Billboard", hue='Artist Efficiency', size= 'Artist Efficiency', data=answer_dff, legend="false")
plt.rcParams['axes.grid'] = True
plt.rcParams['savefig.transparent'] = True
plt.show()








