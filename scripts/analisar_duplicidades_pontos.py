# -*- coding: utf-8 -*-
import glob, os
import geopandas as gpd
from scipy.spatial import cKDTree
import numpy as np

files = sorted(glob.glob('camadas/*.geojson'))

for f in files:
    if any(k in f for k in ['ucs', 'queimada', 'localizacao']):
        continue
    gdf = gpd.read_file(f)
    if len(gdf) == 0 or gdf.geom_type.iloc[0] != 'Point':
        continue
    gdf_utm = gdf.to_crs(epsg=31982)
    coords = np.array([(p.x, p.y) for p in gdf_utm.geometry])
    tree = cKDTree(coords)
    pairs = list(tree.query_pairs(r=35.0))
    print(f"\n==========================================")
    print(f"Camada: {os.path.basename(f)} (Total: {len(gdf)} pontos)")
    print(f"Pares a menos de 35 metros: {len(pairs)}")
    for i, j in pairs[:20]:
        p1 = gdf.iloc[i]
        p2 = gdf.iloc[j]
        d = np.linalg.norm(coords[i] - coords[j])
        n1 = p1.get('nome', '') or ''
        n2 = p2.get('nome', '') or ''
        sub1 = p1.get('subcategoria', '') or ''
        sub2 = p2.get('subcategoria', '') or ''
        print(f"  [{d:.1f}m] ID {p1.get('id')}: '{n1}' ({sub1})  <-->  ID {p2.get('id')}: '{n2}' ({sub2})")
