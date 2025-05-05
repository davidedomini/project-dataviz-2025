import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carica i dati
folder = 'data'
races = pd.read_csv(f'{folder}/races.csv')
driver_standings = pd.read_csv(f'{folder}/driver_standings.csv')

# Unisci le tabelle
merged = driver_standings.merge(races[['raceId', 'year']], on='raceId')

# Filtra per i campioni (posizione 1)
champions = merged[merged['position'] == 1]

# Rimuovi duplicati per anno
champions = champions.drop_duplicates(subset=['year'])

# Ordina per anno
champions = champions.sort_values('year')

# Grafico
plt.figure(figsize=(12,6))
sns.lineplot(data=champions, x='year', y='points', marker='o')
plt.title('Points of World Champions (1950-2022)')
plt.xlabel('Year')
plt.ylabel('Points')
plt.grid(True)
plt.tight_layout()
plt.savefig(
    'charts/world_champion_points.pdf',
    dpi=300,
)

# Conta il numero di gare per anno
races_per_year = races.groupby('year').size().reset_index(name='num_races')

# Grafico
plt.figure(figsize=(12,6))
sns.barplot(data=races_per_year, x='year', y='num_races', palette='Blues_d')
plt.title('Races per Year (1950-2022)')
plt.xlabel('Year')
plt.ylabel('Number of Races')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(
    'charts/races_per_year.pdf',
    dpi=300,
)

# Carica i dati
results = pd.read_csv(f'{folder}/results.csv')
status = pd.read_csv(f'{folder}/status.csv')
circuits = pd.read_csv(f'{folder}/circuits.csv')

# Unisci le tabelle
results_status = results.merge(status, on='statusId')
races_circuits = races[['raceId', 'circuitId']].merge(circuits[['circuitId', 'name']], on='circuitId')
results_full = results_status.merge(races_circuits, on='raceId')

# Filtra per incidenti
incident_keywords = ['Accident', 'Collision', 'Spun off', 'Spun Off', 'Crash']
incidents = results_full[results_full['status'].str.contains('|'.join(incident_keywords), case=False, na=False)]

# Conta gli incidenti per circuito
incidents_per_circuit = incidents['name'].value_counts().reset_index()
incidents_per_circuit.columns = ['Circuit', 'Number of Incidents']

# Grafico
plt.figure(figsize=(12,6))
sns.barplot(data=incidents_per_circuit.head(10), x='Number of Incidents', y='Circuit', palette='Reds_d')
plt.title('Top 10 Circuits by Number of Incidents (1950-2022)')
plt.xlabel('Number of Incidents')
plt.ylabel('Circuit')
plt.tight_layout()
plt.savefig(
    'charts/incidents_per_circuit.pdf',
    dpi=300,
)


# Carica i dati
constructor_standings = pd.read_csv(f'{folder}/constructor_standings.csv')
constructors = pd.read_csv(f'{folder}/constructors.csv')

# Unisci le tabelle
constructor_standings = constructor_standings.merge(races[['raceId', 'year']], on='raceId')
constructor_standings = constructor_standings.merge(constructors[['constructorId', 'name']], on='constructorId')

# Somma i punti per team e anno
points_per_team_year = constructor_standings.groupby(['year', 'name'])['points'].sum().reset_index()

# Filtra per anni recenti (ad esempio, dal 2010 in poi)
recent_years = points_per_team_year[points_per_team_year['year'] >= 2010]

# Pivot per grafico a barre impilate
pivot = recent_years.pivot(index='year', columns='name', values='points').fillna(0)

# Grafico
pivot.plot(kind='bar', stacked=True, figsize=(12,6))
plt.title('Points per Team (2010 - 2022)')
plt.xlabel('Year')
plt.ylabel('Points')
plt.legend(title='Team', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(
    'charts/constructor_points_stacked.pdf',
    dpi=300,
)