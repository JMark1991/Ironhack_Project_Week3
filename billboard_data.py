import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os.path
import time

# web scraping and cleaning the billboard historical data


def create_dates(startDate):
    # creates a csv file (dates.csv) with a series of dates from the startDate provided till '2020-07-11
    day = datetime.datetime.strptime('2020-07-11', '%Y-%m-%d').date()
    start = datetime.datetime.strptime(startDate, '%Y-%m-%d').date()
    weekly_chart_dates = []

    while day >= start:
        weekly_chart_dates.append(str(day))
        day -= datetime.timedelta(weeks=1)

    dateSeries = pd.Series(weekly_chart_dates)
    dateSeries.to_csv('Billboard/dates.csv', index=False)
    print(dateSeries[0], len(dateSeries))

#debug: create a new dates.csv
#create_dates('1960-01-02')



def scrape_week_chart(chart_date):

    # input: chart date (string)
    # output: pandas DataFrame with the top 100 of that week

    url = 'https://www.billboard.com/charts/hot-100/' + chart_date
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features='lxml')
    
    song_name = soup.find_all('span', {'chart-element__information__song text--truncate color--primary'})
    artist_name = soup.find_all('span', {'class': 'chart-element__information__artist text--truncate color--secondary'})
    top100_dict = []
    for n in range(len(artist_name)):

        top100_dict.append(
            {'id':n,
            'Top':n+1,
            'Song_Name':song_name[n].get_text(),
            'Artist_Name':artist_name[n].get_text(),
            'Date': chart_date
            })
    return chart_date, pd.DataFrame(top100_dict)


def write_week_chart_to_file():
    #debug: pass in a fixed date
    #day = '1960-01-02'

    dates = pd.read_csv('Billboard/dates.csv')
    day = dates.values[0][0]
 
    try:    
        scraped_day, df = scrape_week_chart(day)
        print('scraped_day: ',scraped_day)

        if scraped_day:
            # check if file exists
            if not os.path.isfile('Billboard/billboards.csv'):
                
                # if file does not exist, create a new dataframe
                df.to_csv('Billboard/billboards.csv', index=False)

            else:
                # if file exist, append the scraped dataframe to it
                        
                billboard_df = pd.read_csv('Billboard/billboards.csv')

                df['id'] = range(len(billboard_df),len(billboard_df)+100)

                billboard_df = billboard_df.append(df)

                billboard_df.to_csv('Billboard/billboards.csv',index=False)
            
            # remove scraped day from csv
            dates = dates[(dates != day).all(1)]
            dates.to_csv('Billboard/dates.csv', index=False)

    except:
        print('Scrapping failed')
        time.sleep(10)


def double_check_dates():
    # billboard
    billboard_df = pd.read_csv('Billboard/billboards.csv')
    bill_dates = billboard_df['Date'].unique()

    # dates
    dates_df = pd.read_csv('Billboard/dates.csv')
    date_list = dates_df['0'].append(pd.Series(bill_dates)).drop_duplicates(keep=False).dropna()
    date_list.to_csv('Billboard/dates.csv', index=False)



for i in range(200):
    write_week_chart_to_file()
