import pandas as pd
pd.set_option('display.precision', 6)
import random
import plotly.graph_objects as go
import plotly.express as px

def add_probabilities(df):
    df['P_WALK'] = (df['BB'] + df['HBP']) / df['PA']
    df['P_1'] = df['1B'] / df['PA']
    df['P_2'] = df['2B'] / df['PA']
    df['P_3'] = df['3B'] / df['PA']
    df['P_HR'] = df['HR'] / df['PA']
    df['P_SACRIFICE'] = (df['SF'] + df['SH']) / df['PA']
    df['P_OUT'] = 1 - (df['P_WALK'] + df['P_1'] + df['P_2'] + df['P_3'] + df['P_HR'] + df['P_SACRIFICE'])
    # df['prob_total'] = df[['P_WALK', 'P_1', 'P_2', 'P_3', 'P_HR', 'P_SACRIFICE', 'P_OUT']].sum(axis=1)

def simulate_at_bat(at_bat):
    rand = random.random()
    
    p_walk = at_bat['P_WALK']
    p_single = p_walk + at_bat['P_1']
    p_double = p_single + at_bat['P_2']
    p_triple = p_double + at_bat['P_3']
    p_hr = p_triple + at_bat['P_HR']
    p_sacrifice = p_hr + at_bat['P_SACRIFICE']
    
    if rand < p_walk:
        return "WALK"
    elif rand < p_single:
        return "SINGLE"
    elif rand < p_double:
        return "DOUBLE"
    elif rand < p_triple:
        return "TRIPLE"
    elif rand < p_hr:
        return "HOME_RUN"
    elif rand < p_sacrifice:
        return "SACRIFICE"
    else:
        return "OUT"

def simulate_game(df):
    scorecard = {}
    scorecard[0] = 0
    runs = 0
    batter_i = -1

    for inning in range(1,10): # INNINGS
        outs = 0 # each inning starts with 0 outs
        bases = 0b000 # each inning starts with empty bases

        while (outs < 3): # BATTERS
            batter_i = (batter_i + 1) % len(df) # cycle through batters
            at_bat = df.iloc[batter_i] # get batter data
            batting_results = simulate_at_bat(at_bat) # simuate at bat
            # print(f"INNING {inning}, OUTS: {outs}, RUNS: {runs}, BASES: {bases:03b}\nBATTER {at_bat['name']} - RESULT {batting_results}\n")
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
        
        scorecard[inning] = runs

    return scorecard


def monte_carlo(df):
    n = 1000
    for _ in range(n):
        scorecard = simulate_game(df)


def main():
    home_batting = pd.read_csv('home_batting.csv')
    away_batting = pd.read_csv('away_batting.csv')

    add_probabilities(home_batting)
    add_probabilities(away_batting)

    monte_carlo(home_batting)

    print(home_batting)
    print(away_batting)

if __name__ == "__main__":
    main()