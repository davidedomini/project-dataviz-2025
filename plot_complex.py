import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

results = pd.read_csv('data/results.csv')
constructors = pd.read_csv('data/constructors.csv')
drivers = pd.read_csv('data/drivers.csv')
races = pd.read_csv('data/races.csv')

# Unione e filtro stagione
merged = results.merge(drivers[['driverId', 'surname']], on='driverId')
merged = merged.merge(constructors[['constructorId', 'name']], on='constructorId')
merged = merged.merge(races[['raceId', 'year']], on='raceId')
season = 2021
season_data = merged[merged['year'] == season]

# Punti per pilota e team
points_per_driver_team = season_data.groupby(['name', 'surname'])['points'].sum().reset_index()
valid_teams = points_per_driver_team['name'].value_counts()
valid_teams = valid_teams[valid_teams == 2].index.tolist()
filtered = points_per_driver_team[points_per_driver_team['name'].isin(valid_teams)]

pairs = []
for team in valid_teams:
    df = filtered[filtered['name'] == team]
    d1, d2 = df.iloc[0], df.iloc[1]
    pairs.append({'team': team, 'driver1': d1['surname'], 'driver2': d2['surname'],
                  'points1': d1['points'], 'points2': d2['points']})

pairs_df = pd.DataFrame(pairs)

# Grafico
plt.figure(figsize=(8, 8))
sns.scatterplot(data=pairs_df, x='points1', y='points2', hue='team', s=100)
plt.plot([0, max(pairs_df['points1'].max(), pairs_df['points2'].max())],
         [0, max(pairs_df['points1'].max(), pairs_df['points2'].max())],
         ls="--", c=".3", label='Parità')
plt.xlabel('Points Driver 1')
plt.ylabel('Points Driver 2')
plt.title(f'Internal comparison between drivers - {season}')
plt.tight_layout()
plt.grid(True)
plt.savefig(
    f'charts/internal_comparison_drivers_{season}.pdf',
    dpi=300,
)
results = pd.read_csv('data/results.csv')
status = pd.read_csv('data/status.csv')
races = pd.read_csv('data/races.csv')

results_status = results.merge(status, on='statusId')
races_short = races[['raceId', 'circuitId', 'year']]
results_status = results_status.merge(races_short, on='raceId')

sankey_data = results_status[results_status['year'] == 2021]
causes = sankey_data.groupby(['circuitId', 'status']).size().reset_index(name='count')
top_causes = causes.sort_values('count', ascending=False).head(20)

circuits_nodes = top_causes['circuitId'].unique().tolist()
status_nodes = top_causes['status'].unique().tolist()
all_nodes = circuits_nodes + status_nodes
node_index = {name: i for i, name in enumerate(all_nodes)}

links = {
    'source': [node_index[c] for c in top_causes['circuitId']],
    'target': [node_index[s] for s in top_causes['status']],
    'value': top_causes['count'].tolist()
}

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_nodes
    ),
    link=dict(
        source=links['source'],
        target=links['target'],
        value=links['value']
    )
)])
fig.update_layout(title_text="Ritiri per Circuito e Causa (2021)", font_size=10)
fig.write_image(
    'charts/sankey_circuiti_ritiri.pdf',
    format='pdf',
    width=800,
    height=600,
)
# Carica i CSV
results = pd.read_csv('data/results.csv')
constructors = pd.read_csv('data/constructors.csv')
drivers = pd.read_csv('data/drivers.csv')
races = pd.read_csv('data/races.csv')

# Merge e filtro per stagione
merged = results.merge(drivers[['driverId', 'surname']], on='driverId')
merged = merged.merge(constructors[['constructorId', 'name']], on='constructorId')
merged = merged.merge(races[['raceId', 'year']], on='raceId')
season = 2021
season_data = merged[merged['year'] == season]

# Punti per pilota per team
points_per_driver_team = season_data.groupby(['name', 'surname'])['points'].sum().reset_index()
valid_teams = points_per_driver_team['name'].value_counts()
valid_teams = valid_teams[valid_teams == 2].index.tolist()
filtered = points_per_driver_team[points_per_driver_team['name'].isin(valid_teams)]

# Prepara dati
rows = []
for team in valid_teams:
    team_data = filtered[filtered['name'] == team].sort_values('points')
    low, high = team_data.iloc[0], team_data.iloc[1]
    rows.append({
        'team': team,
        'driver1': low['surname'],
        'driver2': high['surname'],
        'points1': low['points'],
        'points2': high['points']
    })

df_plot = pd.DataFrame(rows)

# Plot
plt.figure(figsize=(10, 8))
for i, row in df_plot.iterrows():
    plt.plot([row['points1'], row['points2']], [row['team'], row['team']], color='gray', linewidth=2)
    plt.scatter(row['points1'], row['team'], color='red', zorder=3)
    plt.scatter(row['points2'], row['team'], color='blue', zorder=3)
    # Etichette piloti
    plt.text(row['points1'] - 1.5, row['team'], row['driver1'], va='center', ha='right', color='red', fontsize=9)
    plt.text(row['points2'] + 1.5, row['team'], row['driver2'], va='center', ha='left', color='blue', fontsize=9)

plt.title(f'Confronto Piloti per Team – Stagione {season} (Dumbbell Plot)')
plt.xlabel('Punti')
plt.ylabel('Team')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()


plt.savefig(
    f'charts/dumbbell_plot_{season}.pdf',
    dpi=300,
)