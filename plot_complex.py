import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib

matplotlib.rcParams.update({'axes.titlesize': 20})
matplotlib.rcParams.update({'axes.labelsize': 18})
matplotlib.rcParams.update({'xtick.labelsize': 15})
matplotlib.rcParams.update({'ytick.labelsize': 15})
matplotlib.rcParams.update({'legend.fontsize': 12})
matplotlib.rcParams.update({'legend.title_fontsize': 12})

# Carica i CSV
results = pd.read_csv('data/results.csv')
constructors = pd.read_csv('data/constructors.csv')
drivers = pd.read_csv('data/drivers.csv')
races = pd.read_csv('data/races.csv')

# Merge e filtro per stagione
merged = results.merge(drivers[['driverId', 'surname']], on='driverId')
merged = merged.merge(constructors[['constructorId', 'name']], on='constructorId')
merged = merged.merge(races[['raceId', 'year']], on='raceId')
season = 2022

season_data = merged[merged['year'] == season]

# Punti per pilota per team
points_per_driver_team = season_data.groupby(['name', 'surname'])['points'].sum().reset_index()
valid_teams = points_per_driver_team['name'].value_counts()
print(f'Valid teams: {valid_teams}')
print('------------------------------------------------------------------------------')
valid_teams = valid_teams.index.tolist()
print(f'Valid teams: {valid_teams}')
filtered = points_per_driver_team[points_per_driver_team['name'].isin(valid_teams)]

# Prepara dati
rows = []
for team in valid_teams:
    team_data = filtered[filtered['name'] == team].sort_values('points')
    print(f'Team: {team_data}') 
    if 'Alfa' in team:
        team_data = team_data[team_data['surname'] != 'Kubica'].sort_values('points')
    elif 'Williams' in team:
        team_data = team_data[team_data['surname'] != 'de Vries'].sort_values('points')
    elif 'Aston' in team:
        team_data = team_data[team_data['surname'] != 'Hülkenberg'].sort_values('points')
        
    low, high = team_data.iloc[0], team_data.iloc[1]
    rows.append({
        'team': team,
        'driver1': low['surname'],
        'driver2': high['surname'],
        'points1': low['points'],
        'points2': high['points']
    })

drivers_nick = {
    'Latifi': 'LAT',
    'Schumacher': 'MSC',
    'Verstappen': 'VER',
    'Hamilton': 'HAM',
    'Alonso': 'ALO',
    'Sainz': 'SAI',
    'Leclerc': 'LEC',
    'Norris': 'NOR',
    'Ricciardo': 'RIC',
    'Bottas': 'BOT',
    'Russell': 'RUS',
    'Ocon': 'OCO',
    'Gasly': 'GAS',
    'Tsunoda': 'TSU',
    'Stroll': 'STR',
    'Vettel': 'VET',
    'Mazepin': 'MAZ',
    'Pérez': 'PER',
    'Giovinazzi': 'GIO',
    'Räikkönen': 'RAI',
    'Albon': 'ALB',
    'Zhou': 'ZHO',
    'Magnussen': 'MAG',
    }

df_plot = pd.DataFrame(rows)
df_plot.to_csv('data/dumbbell_plot.csv', index=False)

norm = mcolors.Normalize(vmin=df_plot[['points1', 'points2']].min().min(), vmax=df_plot[['points1', 'points2']].max().max())
cmap = cm.viridis
# Plot
fig, ax = plt.subplots(figsize=(12, 8))
for i, row in df_plot.iterrows():
    color1 = cmap(norm(row['points1']))
    color2 = cmap(norm(row['points2']))
    plt.plot([row['points1'], row['points2']], [row['team'], row['team']], color='gray', linewidth=2)
    plt.scatter(row['points1'], row['team'], color=color1, zorder=3)
    plt.scatter(row['points2'], row['team'], color=color2, zorder=3)
    # Etichette piloti
    plt.text(row['points1'] - 1.5, row['team'], drivers_nick[row['driver1']], va='center', ha='right', color='black', fontsize=12,rotation=45)
    plt.text(row['points2'] + 1.5, row['team'], drivers_nick[row['driver2']], va='center', ha='left', color='black', fontsize=12,rotation=45)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
plt.colorbar(sm, ax=ax, label='Points')  # <-- questa è la legenda dei colori


plt.title(f'')
plt.xlabel('Points')
plt.ylabel('Team')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()


plt.savefig(
    f'charts/dumbbell_plot_{season}.pdf',
    dpi=300,
)