


# Loading and cleaning the spotify data

import pandas as pd


#create DataFrame and print head
#def clean_spotify_data(): 
    

spotify_df= pd.read_csv("Spotify/data.csv")
print(spotify_df.dtypes)

#Transform the dtype of the column year to numeric so I can apply condition in sliccing

spotify_df["year"] = pd.to_numeric(spotify_df["year"])

#Create condition
condition = spotify_df["year"] >= 1960

#Apply Condition to dataframe
spotify_df = spotify_df[condition]

#print head to confirm if condition was applied
print(spotify_df["year"].head())

#change dtype of column "year" from float to int
spotify_df["year"] = spotify_df["year"].astype(int)

#confirm the column is in dtype int64
print(spotify_df["year"].head())


print(spotify_df['artists'])