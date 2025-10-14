import pandas as pd

def add_probabilities(df):
    df['P_WALK'] = (df['BB'] + df['HBP']) / df['PA']
    df['P_1'] = df['1B'] / df['PA']
    df['P_2'] = df['2B'] / df['PA']
    df['P_3'] = df['3B'] / df['PA']
    df['P_HR'] = df['HR'] / df['PA']
    df['P_OUT'] = 1 - (df['P_WALK'] + df['P_1'] + df['P_2'] + df['P_3'] + df['P_HR'])

def get_batting_result(at_bat):
    pass

def simulate_game(df):

    df['pos'] = 0
    runs = 0
    batter_i = -1

    for j in range(9): # INNINGS
        outs = 0

        while (outs < 3): # BATTERS
            batter_i = (batter_i + 1) % len(df)
            at_bat = df.iloc[batter_i]
            batting_results = get_batting_result(at_bat)

            outs += 1

            if batting_results == "OUT":
                outs += 1
                continue

            if batting_results == "WALK":
                pass

            if batting_results == "SINGLE":
                df.loc[df['pos'] > 0, 'pos'] += 1

            if batting_results == "DOUBLE":
                df.loc[df['pos'] > 0, 'pos'] += 2

            if batting_results == "TRIPLE":
                df.loc[df['pos'] > 0, 'pos'] += 3

            if batting_results == "HOME_RUN":
                df.loc[df['pos'] > 0, 'pos'] += 4

def main():
    home_batting = pd.read_csv('home_batting.csv')
    away_batting = pd.read_csv('away_batting.csv')

    add_probabilities(home_batting)
    add_probabilities(away_batting)

    simulate_game(home_batting)

    print(home_batting)
    print(away_batting)

if __name__ == "__main__":
    main()