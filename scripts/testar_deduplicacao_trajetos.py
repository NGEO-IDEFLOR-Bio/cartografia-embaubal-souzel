import subprocess, json
import numpy as np
from scipy.spatial import cKDTree
import geopandas as gpd

out = subprocess.check_output(['git', 'show', '1c53a73:camadas/10_trajetos_e_acessos.geojson']).decode('utf-8')
data = json.loads(out)
features = data['features']

records = []
for f in features:
    p = f['properties']
    coords = f['geometry']['coordinates']
    records.append({
        'id': p.get('id'),
        'nome': p.get('nome'),
        'alt': p.get('nome_alternativo'),
        'obs': p.get('observacoes'),
        'fonte': p.get('fonte'),
        'lon': coords[0],
        'lat': coords[1]
    })

gdf = gpd.GeoDataFrame(records, geometry=gpd.points_from_xy([r['lon'] for r in records], [r['lat'] for r in records]), crs='EPSG:4674')
gdf_utm = gdf.to_crs(epsg=31982)

# 1. Filtra almoços
gdf_sem_almoco = gdf_utm[~gdf_utm['nome'].str.contains('almo', case=False, na=False)].copy()
print(f"Total sem almoço: {len(gdf_sem_almoco)}")

# 2. Agrupa por proximidade espacial (raio 40m)
coords = np.array([(p.x, p.y) for p in gdf_sem_almoco.geometry])
tree = cKDTree(coords)
pairs = tree.query_pairs(r=40.0)

# Agrupamento conexo
from scipy.sparse.csgraph import connected_components
from scipy.sparse import lil_matrix

n = len(gdf_sem_almoco)
adj = lil_matrix((n, n), dtype=int)
for i, j in pairs:
    adj[i, j] = 1
    adj[j, i] = 1

n_components, labels = connected_components(adj)
print(f"Agrupamentos espaciais únicos: {n_components}")

gdf_sem_almoco['cluster'] = labels

# Para cada cluster, seleciona 1 ponto representativo (centróide ou primeiro ponto com melhor descrição)
pontos_unicos = []
for cl in range(n_components):
    sub = gdf_sem_almoco[gdf_sem_almoco['cluster'] == cl]
    rep = sub.iloc[0]
    pontos_unicos.append({
        'id': rep['id'],
        'nome_orig': rep['nome'],
        'alt': rep['alt'],
        'qtd_passadas': len(sub),
        'geometry': rep.geometry
    })

gdf_rep = gpd.GeoDataFrame(pontos_unicos, geometry='geometry', crs=gdf_sem_almoco.crs).to_crs(epsg=4674)
print(f"\nPontos representativos finais de trajetos: {len(gdf_rep)}")
for i, r in gdf_rep.iterrows():
    print(f"  Ponto {i+1:2d} (ID {r['id']}, {r['qtd_passadas']} passadas): [{r.geometry.x:.5f}, {r.geometry.y:.5f}] - orig: {r['nome_orig']}")
