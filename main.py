import pandas as pd
pd.set_option('display.precision', 6)

def add_probabilities(df):
    df['P_WALK'] = (df['BB'] + df['HBP']) / df['PA']
    df['P_1'] = df['1B'] / df['PA']
    df['P_2'] = df['2B'] / df['PA']
    df['P_3'] = df['3B'] / df['PA']
    df['P_HR'] = df['HR'] / df['PA']
    df['P_SACRIFICE'] = (df['SF'] + df['SH']) / df['PA']
    df['P_OUT'] = 1 - (df['P_WALK'] + df['P_1'] + df['P_2'] + df['P_3'] + df['P_HR'] + df['P_SACRIFICE'])
    df['prob_total'] = df[['P_WALK', 'P_1', 'P_2', 'P_3', 'P_HR', 'P_SACRIFICE', 'P_OUT']].sum(axis=1)

def simulate_at_bat(at_bat):
    return "OUT"

def simulate_game(df):
    runs = 0
    batter_i = -1

    for _ in range(9): # INNINGS
        outs = 0 # each inning starts with 0 outs
        bases = 0b000 # each inning starts with empty bases

        while (outs < 3): # BATTERS
            batter_i = (batter_i + 1) % len(df) # cycle through batters
            at_bat = df.iloc[batter_i] # get batter data
            batting_results = simulate_at_bat(at_bat) # simuate at bat

            if batting_results == "OUT":
                outs += 1
                continue

            if batting_results == "SACRIFICE":
                outs += 1
                if outs >= 3:
                    continue
                match bases:
                    case 0b000:
                        pass
                    case 0b001:
                        bases = 0b010
                    case 0b010:
                        bases = 0b100
                    case 0b011:
                        bases = 0b110
                    case 0b100:
                        bases = 0b000
                        runs += 1
                    case 0b101:
                        bases = 0b010
                        runs += 1
                    case 0b110:
                        bases = 0b100
                        runs += 1
                    case 0b111:
                        bases = 0b110
                        runs += 1
                continue

            if batting_results == "WALK":
                match bases:
                    case 0b000:
                        bases = 0b001
                    case 0b001:
                        bases = 0b011
                    case 0b010:
                        bases = 0b011
                    case 0b011:
                        bases = 0b111
                    case 0b100:
                        bases = 0b101
                    case 0b101:
                        bases = 0b111
                    case 0b110:
                        bases = 0b111
                    case 0b111:
                        bases = 0b111
                        runs += 1
                continue

            if batting_results == "SINGLE":
                match bases:
                    case 0b000:
                        bases = 0b001
                    case 0b001:
                        bases = 0b011
                    case 0b010:
                        bases = 0b101
                    case 0b011:
                        bases = 0b111
                    case 0b100:
                        bases = 0b001
                        runs += 1
                    case 0b101:
                        bases = 0b011
                        runs += 1
                    case 0b110:
                        bases = 0b101
                        runs += 1
                    case 0b111:
                        bases = 0b111
                        runs += 1
                continue

            if batting_results == "DOUBLE":
                match bases:
                    case 0b000:
                        bases = 0b010
                    case 0b001:
                        bases = 0b110
                    case 0b010:
                        bases = 0b010
                        runs += 1
                    case 0b011:
                        bases = 0b110
                        runs += 1
                    case 0b100:
                        bases = 0b010
                        runs += 1
                    case 0b101:
                        bases = 0b110
                        runs += 1
                    case 0b110:
                        bases = 0b010
                        runs += 2
                    case 0b111:
                        bases = 0b110
                        runs += 2
                continue

            if batting_results == "TRIPLE":
                match bases:
                    case 0b000:
                        pass
                    case 0b001:
                        runs += 1
                    case 0b010:
                        runs += 1
                    case 0b011:
                        runs += 2
                    case 0b100:
                        runs +=1 
                    case 0b101:
                        runs += 2
                    case 0b110:
                        runs += 2
                    case 0b111:
                        runs += 3
                bases = 0b100
                continue

            if batting_results == "HOME_RUN":
                match bases:
                    case 0b000:
                        runs += 1
                    case 0b001:
                        runs += 2
                    case 0b010:
                        runs += 2
                    case 0b011:
                        runs += 3
                    case 0b100:
                        runs += 2
                    case 0b101:
                        runs += 3
                    case 0b110:
                        runs += 3
                    case 0b111:
                        runs += 4
                bases = 0b000
                continue

def main():
    home_batting = pd.read_csv('home_batting.csv')
    away_batting = pd.read_csv('away_batting.csv')

    add_probabilities(home_batting)
    add_probabilities(away_batting)

    simulate_game(home_batting)

    print(home_batting.iloc[:, 10:])
    print(away_batting.iloc[:, 10:])

if __name__ == "__main__":
    main()