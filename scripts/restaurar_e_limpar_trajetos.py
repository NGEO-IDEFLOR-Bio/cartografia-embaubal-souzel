# -*- coding: utf-8 -*-
"""
Restauração, Limpeza Toponímica e Deduplicação da Camada 10_trajetos_e_acessos.geojson
Garante que a camada mantenha geometria válida de Ponto (Point) no QGIS,
eliminando pontos de refeição ('almoço'), unificando passadas no mesmo local
e atribuindo nomenclatura cartográfica técnica oficial.
"""

import os
import subprocess
import json
import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components
from scipy.sparse import lil_matrix

# 1. Recupera os dados originais preservados no histórico do Git
out = subprocess.check_output(['git', 'show', '1c53a73:camadas/10_trajetos_e_acessos.geojson']).decode('utf-8')
data = json.loads(out)
features = data['features']
print(f"Total de feições recuperadas do histórico: {len(features)}")

# 2. Converte para GeoDataFrame
records = []
for f in features:
    p = f['properties']
    coords = f['geometry']['coordinates']
    records.append({
        'id': p.get('id'),
        'nome_original': p.get('nome', ''),
        'subcategoria': p.get('subcategoria', 'Trajetos e Acessos'),
        'observacoes': p.get('observacoes', ''),
        'data_coleta': p.get('data_coleta', ''),
        'fonte': p.get('fonte', 'Lorena / Kelly (Campo)'),
        'lon': coords[0],
        'lat': coords[1]
    })

gdf = gpd.GeoDataFrame(
    records,
    geometry=gpd.points_from_xy([r['lon'] for r in records], [r['lat'] for r in records]),
    crs='EPSG:4674'
)
gdf_utm = gdf.to_crs(epsg=31982)

# 3. Elimina pontos espúrios de parada para refeição ('almoço')
mask_almoco = gdf_utm['nome_original'].str.contains('almo', case=False, na=False)
qtd_almoco = int(mask_almoco.sum())
gdf_sem_almoco = gdf_utm[~mask_almoco].copy().reset_index(drop=True)
print(f"Pontos de almoço eliminados: {qtd_almoco}")

# 4. Agrupa passadas múltiplas no mesmo local físico (tolerância euclidiana de 40 metros)
coords = np.array([(p.x, p.y) for p in gdf_sem_almoco.geometry])
tree = cKDTree(coords)
pairs = tree.query_pairs(r=40.0)

n = len(gdf_sem_almoco)
adj = lil_matrix((n, n), dtype=int)
for i, j in pairs:
    adj[i, j] = 1
    adj[j, i] = 1

n_components, labels = connected_components(adj)
gdf_sem_almoco['cluster'] = labels

# 5. Seleciona 1 ponto representativo por sítio geográfico e atribui toponímia técnica
pontos_homologados = []
ponto_idx = 1

for cl in range(n_components):
    sub = gdf_sem_almoco[gdf_sem_almoco['cluster'] == cl]
    rep = sub.iloc[0]
    
    # Identifica nome toponímico contextualizado
    orig = rep['nome_original']
    
    # Casos especiais conhecidos pela localização
    if rep['id'] in [486, 523, 553, 564, 565]:
        nome_tecnico = "Ponto de Acesso / Atracadouro – Base Fluvial IDEFLOR-Bio"
        subcat = "Atracadouros e Portos"
    elif 'pesca' in orig.lower():
        nome_tecnico = f"Ponto de Acesso / Pesqueiro Fluvial {ponto_idx:02d}"
        subcat = "Acesso Pesqueiro"
    elif 'corrida' in orig.lower() or 'trilha' in orig.lower() or 'caminhando' in orig.lower():
        nome_tecnico = f"Ponto de Acesso a Trilha / Monitoramento {ponto_idx:02d}"
        subcat = "Trilhas e Varadouros"
    else:
        nome_tecnico = f"Ponto de Acesso e Monitoramento Fluvial {ponto_idx:02d}"
        subcat = "Acessos Fluviais"
        
    pontos_homologados.append({
        'id': rep['id'],
        'nome': nome_tecnico,
        'categoria': 'Trajetos e Acessos',
        'subcategoria': subcat,
        'unidade_conservacao': 'REVIS Tabuleiro do Embaubal / RDS Vitória de Souzel',
        'nome_alternativo': f"Registro original de campo: {orig}",
        'observacoes': f"Ponto representativo homologado após unificação de {len(sub)} passada(s) de campo.",
        'data_coleta': rep['data_coleta'],
        'fonte': rep['fonte'],
        'latitude': round(rep.geometry.y, 6),
        'longitude': round(rep.geometry.x, 6),
        'geometry': rep.geometry
    })
    ponto_idx += 1

gdf_final = gpd.GeoDataFrame(pontos_homologados, geometry='geometry', crs=gdf_sem_almoco.crs).to_crs(epsg=4674)
gdf_final['latitude'] = gdf_final.geometry.y.round(6)
gdf_final['longitude'] = gdf_final.geometry.x.round(6)

print(f"Total de pontos de acessos homologados com geometria válida: {len(gdf_final)}")

# Salva arquivo GeoJSON com geometria de Pontos garantida
fpath_trajetos = "camadas/10_trajetos_e_acessos.geojson"
gdf_final.to_file(fpath_trajetos, driver="GeoJSON", encoding="utf-8")
print(f"[OK] Arquivo salvo com sucesso: {fpath_trajetos} ({len(gdf_final)} feições do tipo Point)")

# 6. Atualiza o consolidado geral de pontos
print("\n--- Atualizando pontos_revis_rds_consolidado (.geojson e .gpkg) ---")
camadas_ativas = [
    '01_moradores_e_comunidades.geojson',
    '02_apoio_de_pesca_e_ranchos.geojson',
    '03_areas_de_desova.geojson',
    '04_hidrografia.geojson',
    '05_ilhas_e_praias.geojson',
    '06_infraestrutura_e_equipamentos.geojson',
    '07_marcos_e_pontos_referencia.geojson',
    '08_vegetacao_e_flora.geojson',
    '09_ocorrencias_e_impactos.geojson',
    '10_trajetos_e_acessos.geojson'
]

gdfs = []
for c in camadas_ativas:
    p = f"camadas/{c}"
    if os.path.exists(p):
        g = gpd.read_file(p)
        if len(g) > 0:
            gdfs.append(g.to_crs(epsg=4674))
            print(f"  + {c}: {len(g)} pontos")

gdf_cons = pd.concat(gdfs, ignore_index=True)
gdf_cons = gpd.GeoDataFrame(gdf_cons, geometry='geometry', crs="EPSG:4674")

gdf_cons.to_file("camadas/pontos_revis_rds_consolidado.geojson", driver="GeoJSON", encoding="utf-8")
gdf_cons.to_file("camadas/pontos_revis_rds_consolidado.gpkg", layer="pontos_campo", driver="GPKG")
print(f"[OK] Consolidado geral atualizado: {len(gdf_cons)} pontos únicos.")
