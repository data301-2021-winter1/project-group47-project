def load_and_process_goals(df):
    season_games_min = 30
    threshold = len(df) * .40
    df = (df.dropna(thresh=threshold, axis=1)
          .drop(['D'], axis=1)
          .dropna(axis=0)
          .sort_values(by=['Pos', 'GD'], ascending=[True, False])
          )
    df1 = df[df['GP'] >= season_games_min]
    df1 = df1[df1['Conference'] == 'Overall']
    return df1


def load_and_process_players(df):
    years = [2000, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
             2014, 2015, 2016, 2017, 2018, 2019]
    df = df[['Player', 'Club', 'G', 'SHTS', 'SOG', 'SOG%', 'Year']]
    df1 = df[df.Year.isin(years) == True]
    df2 = (df1.sort_values(by=['Player', 'Year'], ascending=[True, True])
           .groupby(['Player', 'Year']).agg({'SHTS': 'sum', 'SOG': 'sum', 'Club': 'sum'})
           )
    return df2


def find_and_delete_duplicates(csv):
    csv =
    if len(csv[csv.duplicated()]) > 0:
        print("No. of duplicated entries: ", len(csv[csv.duplicated()]))
        print(csv[csv.duplicated(keep=False)].sort_values(
            by=list(csv.columns)).head())
        csv.drop_duplicates(inplace=True)
    else:
        print("No duplicated entries found")
    return csv
