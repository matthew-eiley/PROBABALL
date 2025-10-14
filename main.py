import pandas as pd

def add_probabilities(df):
    df['P_1'] = (df['1B'] + df['BB'] + df['HBP']) / df['PA']
    df['P_2'] = df['2B'] / df['PA']
    df['P_3'] = df['3B'] / df['PA']
    df['P_HR'] = df['HR'] / df['PA']
    df['P_OUT'] = 1 - (df['P_1'] + df['P_2'] + df['P_3'] + df['P_HR'])

def main():
    home_batting = pd.read_csv('home_batting.csv')
    away_batting = pd.read_csv('away_batting.csv')

    add_probabilities(home_batting)
    add_probabilities(away_batting)

    print(home_batting)
    print(away_batting)

if __name__ == "__main__":
    main()