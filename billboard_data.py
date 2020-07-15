import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

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
create_dates('1960-01-02')



def scrape_week_chart(chart_date):

    # input: chart date (string)
    # output: pandas DataFrame with the top 100 of that week

    try:
        url = 'https://www.billboard.com/charts/hot-100/' + chart_date
        response = requests.get(url)
        soup = BeautifulSoup(response.content, features='lxml')
        
        song_name = soup.find_all('span', {'chart-element__information__song text--truncate color--primary'})
        artist_name = soup.find_all('span', {'class': 'chart-element__information__artist text--truncate color--secondary'})

        top100_dict = []
        for n in range(100):
            top100_dict.append(
                {'Top':n+1,
                'Song_Name':song_name[n].get_text(),
                'Artist_Name':artist_name[n].get_text(),
                'Date': chart_date
                })

        return chart_date, pd.DataFrame(top100_dict)
    except:
        pass


day = '1960-01-02'
scraped_day, df = scrape_week_chart(day)

if scraped_day:
    # remove scraped day from csv
    dates = pd.read_csv('Billboard/dates.csv')
    dates = dates[(dates != day).all(1)]
    dates.to_csv('Billboard/dates.csv', index=False)

    # append the scraped dataframe to the existing
    billboard_df = pd.read_csv('Billboard/billboards.csv',index_col='Top')
    billboard_df.append(df)
    billboard_df.to_csv('Billboard/billboards.csv', index='Top')

    #debug: create a new dataframe
    #df.to_csv('Billboard/billboards.csv', index=False)




