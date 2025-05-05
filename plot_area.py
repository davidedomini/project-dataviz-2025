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

# Calcola i punti totali per ogni team per anno
team_points = recent.groupby(['year', 'name'])['points'].sum().reset_index()

# Trova i 5 team con più punti complessivi in 10 anni
top_teams = team_points.groupby('name')['points'].sum().nlargest(5).index.tolist()
team_points = team_points[team_points['name'].isin(top_teams)]

# Pivot per area chart
pivot = team_points.pivot(index='year', columns='name', values='points').fillna(0)


# pivot_percent = pivot.div(pivot.sum(axis=1), axis=0)

# Grafico area
pivot.plot(kind='area', stacked=True, figsize=(12, 6), alpha=0.8)

plt.title('Points for top teams (2014–2023)')

plt.xlabel('Year')
plt.ylabel('Points %')
plt.legend(title='Team', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(
    'charts/top_teams_area_chart.pdf',
    dpi=300,
)