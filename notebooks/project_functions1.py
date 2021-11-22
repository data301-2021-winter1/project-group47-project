import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns


def load_and_process_goals(df):
    df = find_and_delete_duplicates(df)
    season_games_min = 30
    threshold = len(df) * .40
    df = (df.dropna(thresh=threshold, axis=1)
          .drop(['D'], axis=1)
          .sort_values(by=['GD'], ascending=[False])
          )
    df = (df.replace(['Los Angeles Galaxy', 'LA Galaxy '],'LA Galaxy')
          .replace(['Kansas City Wizards', 'Kansas City Wizards ', 'Kansas City Wiz'],'Sporting Kansas City')
          .replace(['Columbus Crew SC'],'Columbus Crew')
          .replace(['San Jose Clash'],'San Jose Earthquakes')
          .replace(['MetroStars ', 'MetroStars', 'NY/NJ MetroStars'],'New York Red Bulls')
          .replace(['49[a]'],'49')
         )
    df1 = df[df['GP'] >= season_games_min]
    df1 = df1[(df1['Conference'] == 'Overall') & (df1['Pos'] == 1.0)]
    return df1


def load_and_process_players(df):
    df = find_and_delete_duplicates(df)
    values = ['CAN','CIV','ECU','GHA','HAI','HON','JAM','MTQ','PAN','USA','ROC','SLV', 'MIA']
    years = [1996, 1997, 2000, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
             2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
    df = df[['Player', 'Club', 'G', 'SHTS', 'SOG', 'SOG%', 'Year']]
    df1 = df[df.Year.isin(years) == True]
    df2 = (df1.replace(['ATL','VAN','CHI','CIN','CHV','CLB','TB ','DAL','COL','HOU','POR','NYC', 'ORL', 'TOR', 'MTL', 'NSH', 'MIN', 'PHI', 'SEA', 'RSL'],['Atlanta United FC','Vancouver Whitecaps FC', 'Chicago Fire', 'FC Cincinnati','Chivas USA','Columbus Crew', 'Tampa Bay Mutiny', 'FC Dallas','Colorado Rapids','Houston Dynamo','Portland Timbers','New York City FC', 'Orlando City SC', 'Toronto FC', 'Montreal Impact', 'Nashville SC', 'Minnesota United FC', 'Philadelphia Union', 'Seattle Sounders FC', 'Real Salt Lake'])
           .replace(['NYC'],'New York City FC')
           .replace(['NYR', 'RBNY', 'MET', 'NY', 'NY ', 'MetroStars'],'New York Red Bulls')
           .replace(['DC', 'DC '],'D.C. United')
           .replace(['NE', 'NE '],'New England Revolution')
           .replace(['SKC', 'KC '],'Sporting Kansas City')
           .replace(['SJ', 'SJ '],'San Jose Earthquakes')
           .replace(['LA', 'LA '],'LA Galaxy')
           .replace(['LAFC', 'LFC'],'Los Angeles FC')
          )
    df3 = df2[df2.Club.isin(values) == False]
    df4 = (df3.sort_values(by=['Player', 'Year'], ascending=[True, True])
           .groupby(['Player', 'Year']).agg({'SHTS': 'sum', 'SOG': 'sum', 'Club': 'sum'})
           .groupby(['Club','Year']).agg({'SHTS': 'sum', 'SOG': 'sum'})
           )
    df4 = df4[df4['SHTS'] > 200]
    df4.rename(columns = {'Club':'Team'}, inplace = True)
    return df4


def find_and_delete_duplicates(csv):
    csv = pd.read_csv(csv)
    if len(csv[csv.duplicated()]) > 0:
        print("No. of duplicated entries: ", len(csv[csv.duplicated()]))
        print(csv[csv.duplicated(keep=False)].sort_values(
            by=list(csv.columns)).head())
        csv.drop_duplicates(inplace=True)
    else:
        print("No duplicated entries found")
    return csv
