import pandas as pd
pd.set_option('display.precision', 6)
import random
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from scipy import stats

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


def simulate_monte_carlo(df, n=1000):
    all_scorecards = []
    for _ in range(n):
        scorecard = simulate_game(df)
        all_scorecards.append(scorecard)
    return all_scorecards


def plot_monte_carlo(all_scorecards, team_name="Team"):
    # Convert scorecards to a format suitable for plotting
    data = []
    for i, scorecard in enumerate(all_scorecards):
        for inning, runs in scorecard.items():
            data.append({'Game': i+1, 'Inning': inning, 'Cumulative_Runs': runs})
    
    df_plot = pd.DataFrame(data)
    
    fig = go.Figure()
    
    # Plot individual games as thin lines with points
    for game_id in df_plot['Game']:#.unique()[:100]:
        game_data = df_plot[df_plot['Game'] == game_id]
        fig.add_trace(go.Scatter(
            x=game_data['Inning'],
            y=game_data['Cumulative_Runs'],
            mode='lines+markers',
            name=f'Game {game_id}',
            line=dict(width=1, color='rgba(0,0,0,0.25)'),
            marker=dict(size=4, color='rgba(0,0,0,0.25)'),
            showlegend=False,
            hovertemplate='<b>Game %{customdata}</b><br>Inning: %{x}<br>Cumulative Runs: %{y}<extra></extra>',
            customdata=[game_id] * len(game_data)
        ))
    
    # Calculate and plot median with larger points
    median_data = df_plot.groupby('Inning')['Cumulative_Runs'].median().reset_index()
    fig.add_trace(go.Scatter(
        x=median_data['Inning'],
        y=median_data['Cumulative_Runs'],
        mode='lines+markers',
        name='MEDIAN',
        line=dict(width=3, color='red'),
        marker=dict(size=12, color='red'),
        hovertemplate='<b>MEDIAN</b><br>Inning: %{x}<br>Cumulative Runs: %{y}<extra></extra>'
    ))
    
    # Calculate and plot mean with larger points
    mean_data = df_plot.groupby('Inning')['Cumulative_Runs'].mean().reset_index()
    fig.add_trace(go.Scatter(
        x=mean_data['Inning'],
        y=mean_data['Cumulative_Runs'],
        mode='lines+markers',
        name='MEAN',
        line=dict(width=3, color='blue'),
        marker=dict(size=12, color='blue'),
        hovertemplate='<b>MEAN</b><br>Inning: %{x}<br>Cumulative Runs: %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'{team_name} Monte Carlo Simulation - Runs by Inning',
        xaxis_title='Inning',
        yaxis_title='Cumulative Runs',
        hovermode='closest',
        width=1200,
        height=800
    )
    
    return fig

def plot_runs_histogram(all_scorecards, team_name="Team"):
    # Extract final runs (inning 9) from each game
    final_runs = [scorecard[9] for scorecard in all_scorecards]
    
    # Calculate statistics
    mean_runs = np.mean(final_runs)
    median_runs = np.median(final_runs)
    std_runs = np.std(final_runs)
    
    # Create histogram
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=final_runs,
        nbinsx=max(final_runs) - min(final_runs) + 1,
        name='Games',
        marker=dict(color='skyblue', opacity=0.7, line=dict(color='black', width=0.5)),
        hovertemplate='Runs: %{x}<br>Count: %{y}<extra></extra>'
    ))
    
    # Add mean line
    fig.add_vline(
        x=mean_runs,
        line_dash="dash",
        line_color="red",
        line_width=2,
        annotation_text=f'Mean: {mean_runs:.2f}',
        annotation_position="top right"
    )
    
    # Add median line
    fig.add_vline(
        x=median_runs,
        line_dash="dash",
        line_color="orange",
        line_width=2,
        annotation_text=f'Median: {median_runs:.2f}',
        annotation_position="top left"
    )
    
    # Add statistics text box
    stats_text = f'Total Games: {len(final_runs)}<br>Min: {min(final_runs)}<br>Max: {max(final_runs)}<br>Std Dev: {std_runs:.2f}'
    
    fig.add_annotation(
        text=stats_text,
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        xanchor="left", yanchor="top",
        showarrow=False,
        bgcolor="white",
        bordercolor="black",
        borderwidth=1
    )
    
    fig.update_layout(
        title=f'{team_name} - Distribution of Total Runs After 9 Innings',
        xaxis_title='Total Runs',
        yaxis_title='Number of Games',
        width=1200,
        height=600,
        showlegend=False
    )
    
    return fig


def main():
    home_batting = pd.read_csv('home_batting.csv')
    away_batting = pd.read_csv('away_batting.csv')

    add_probabilities(home_batting)
    add_probabilities(away_batting)

    all_scorecards = simulate_monte_carlo(home_batting, 2000)
    
    fig1 = plot_monte_carlo(all_scorecards, team_name="home_batting")
    fig1.show()
    
    fig2 = plot_runs_histogram(all_scorecards, team_name="home_batting")
    fig2.show()


if __name__ == "__main__":
    main()