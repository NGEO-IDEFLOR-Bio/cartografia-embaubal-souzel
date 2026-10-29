import subprocess, json
import numpy as np
from scipy.spatial import cKDTree
import geopandas as gpd

out = subprocess.check_output(['git', 'show', '1c53a73:camadas/10_trajetos_e_acessos.geojson']).decode('utf-8')
data = json.loads(out)

features = data['features']
print(f"Total features: {len(features)}")

# Cria GeoDataFrame
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

# Clusteriza pontos próximos (distância <= 100m)
coords = np.array([(p.x, p.y) for p in gdf_utm.geometry])
tree = cKDTree(coords)
pairs = tree.query_pairs(r=80.0)

print(f"Pares a menos de 80m: {len(pairs)}")

# Identifica pontos com 'almoço'
almoco = [r for r in records if 'almo' in (r['nome'] or '').lower()]
print(f"\nPontos de almoço identificados ({len(almoco)}):")
for r in almoco:
    print(f"  ID {r['id']}: {r['nome']} at [{r['lon']}, {r['lat']}]")
