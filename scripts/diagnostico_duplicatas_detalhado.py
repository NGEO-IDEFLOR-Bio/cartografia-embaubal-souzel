# -*- coding: utf-8 -*-
import glob, os
import geopandas as gpd
from scipy.spatial import cKDTree
import numpy as np
import difflib

def similaridade(s1, s2):
    return difflib.SequenceMatcher(None, str(s1).lower(), str(s2).lower()).ratio()

files = [
    'camadas/01_moradores_e_comunidades.geojson',
    'camadas/02_apoio_de_pesca_e_ranchos.geojson',
    'camadas/03_areas_de_desova.geojson',
    'camadas/04_hidrografia.geojson',
    'camadas/05_ilhas_e_praias.geojson',
    'camadas/06_infraestrutura_e_equipamentos.geojson',
    'camadas/07_marcos_e_pontos_referencia.geojson',
    'camadas/08_vegetacao_e_flora.geojson',
    'camadas/09_ocorrencias_e_impactos.geojson',
    'camadas/10_trajetos_e_acessos.geojson'
]

for f in files:
    if not os.path.exists(f): continue
    gdf = gpd.read_file(f)
    if len(gdf) == 0: continue
    
    gdf_utm = gdf.to_crs(epsg=31982)
    coords = np.array([(p.x, p.y) for p in gdf_utm.geometry])
    tree = cKDTree(coords)
    
    # Busca pares a menos de 30m
    pairs = tree.query_pairs(r=30.0)
    
    dups_certos = []
    for i, j in pairs:
        p1 = gdf.iloc[i]
        p2 = gdf.iloc[j]
        d = np.linalg.norm(coords[i] - coords[j])
        n1 = str(p1.get('nome', '') or '').strip()
        n2 = str(p2.get('nome', '') or '').strip()
        sim = similaridade(n1, n2)
        
        # Critérios de duplicidade clara:
        # 1. Distância < 2m (mesmo ponto exato)
        # 2. Distância < 30m e nomes similares (> 0.5) ou ambos 'desconhecido' ou um contém o outro
        if d < 3.0 or sim > 0.45 or (n1.lower() in n2.lower()) or (n2.lower() in n1.lower()):
            dups_certos.append((i, j, d, sim, n1, n2, p1.get('id'), p2.get('id')))
            
    print(f"\n=======================================================")
    print(f"Camada: {os.path.basename(f)} (Total: {len(gdf)} pontos)")
    print(f"Duplicatas detectadas (mesma feição / passada múltipla): {len(dups_certos)}")
    for i, j, d, sim, n1, n2, id1, id2 in sorted(dups_certos, key=lambda x: x[2]):
        print(f"  [{d:4.1f}m] ID {id1} ('{n1}')  ==  ID {id2} ('{n2}')")
