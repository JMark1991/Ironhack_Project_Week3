

Objective:
Load the data from the 2 sources (spotify data from kaggle, billboard charts)
Merge the 2 tables (probably by Song Name)
Analyse how the songs variables have changed over time

IDEAS:

» weighted  average of the variables of each song vs popularity_score, and for each variable per year
    danceability, energy, acousticness, instrumentalness, liveness, speechiness, loudness, valence  

» % explicits per decade

» % songs that became popular per artist

» artists with the biggest average for each variable (per decade)

» which decades are more popular according to spotify popularity - not interesting

TO DO:

Spotify Data:
    Save the file - done
    Read to spotify_data.py - done
    Clean it if needed - done
    Return a Dataframe - done

Billboard Data:
    Webscrape the data and save it to a file (may require several times) - done
    Read from file - done
    Clean if needed - done
    Aggregate the data by year (maybe by decade) - done
    Return a DataFrame - done

Song_id:
    Find the spotify ids of each music in the billboards - done
    Replace the temporary_id with the spotify_id 



Graph out the different variables over time
Take conclusions
Make presentation
