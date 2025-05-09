import pandas as pd
import matplotlib.pyplot as plt

# Carica i CSV (modifica il path se servono)
constructor_standings = pd.read_csv('data/constructor_standings.csv')
races = pd.read_csv('data/races.csv')
constructors = pd.read_csv('data/constructors.csv')

# Unisci tabelle per ottenere year e nome team
merged = constructor_standings.merge(races[['raceId', 'year']], on='raceId')
merged = merged.merge(constructors[['constructorId', 'name']], on='constructorId')

# Filtra per gli ultimi 10 anni
recent = merged[merged['year'].between(2014, 2023)]
max_raceid_idx = recent.groupby(['name', 'year'])['raceId'].idxmax()
recent = recent.loc[max_raceid_idx].reset_index(drop=True)
# print(max_raceid_idx)
# recent.to_csv('diocane.csv', index=False)

# Calcola i punti totali per ogni team per anno
print(recent)

team_points = recent.groupby(['year', 'name'])['points'].sum().reset_index()
print(team_points)

# Trova i 5 team con più punti complessivi in 10 anni
top_teams = team_points.groupby('name')['points'].sum().nlargest(5).index.tolist()
team_points = team_points[team_points['name'].isin(top_teams)]

# Pivot per area chart
pivot = team_points.pivot(index='year', columns='name', values='points').fillna(0)

pivot.to_csv('data/top_teams_pivot.csv')

# pivot_percent = pivot.div(pivot.sum(axis=1), axis=0)

color_map = {
    'Ferrari': '#4c72b0',
    'Mercedes': '#dd8452',
    'Red Bull': '#55a868',
    'McLaren': '#c44e52',
    'Williams': '#8172b3',
}

colors = [color_map.get(col, 'black') for col in pivot.columns]

# Grafico area
pivot.plot(kind='area', stacked=True, figsize=(12, 6), alpha=0.8, color=colors)

plt.title('Points for top teams (2014-2023)')

plt.xlabel('Year')
plt.ylabel('Points')
plt.legend(title='Team', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(
    'charts/top_teams_area_chart.pdf',
    dpi=300,
)