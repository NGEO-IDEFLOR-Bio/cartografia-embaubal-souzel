# -*- coding: utf-8 -*-
import os, glob
import geopandas as gpd
from scipy.spatial import cKDTree
import numpy as np
import difflib

def score_qualidade_nome(nome):
    s = str(nome or '').strip()
    if not s: return -10
    sl = s.lower()
    if sl in ['desconhecido', 'abandonado', 'rancho desconhecido', 'sem nome']: return 0
    if sl.isdigit(): return 1
    # Mais longo e com mais palavras geralmente é mais descritivo/completo
    return 10 + len(s) + (s.count(' ') * 5)

def encontrar_duplicatas_camada(gdf, dist_limite=25.0):
    gdf_utm = gdf.to_crs(epsg=31982)
    coords = np.array([(p.x, p.y) for p in gdf_utm.geometry])
    tree = cKDTree(coords)
    pairs = tree.query_pairs(r=dist_limite)
    
    indices_para_remover = set()
    pares_resolvidos = []
    
    for i, j in pairs:
        if i in indices_para_remover or j in indices_para_remover:
            continue
        p1 = gdf.iloc[i]
        p2 = gdf.iloc[j]
        d = np.linalg.norm(coords[i] - coords[j])
        
        n1 = str(p1.get('nome', '') or '').strip()
        n2 = str(p2.get('nome', '') or '').strip()
        
        sim = difflib.SequenceMatcher(None, n1.lower(), n2.lower()).ratio()
        
        # Critérios para considerar a mesma passada / mesmo local:
        eh_duplicata = False
        if d <= 5.0:
            eh_duplicata = True
        elif d <= dist_limite:
            if sim > 0.40 or (n1.lower() in n2.lower()) or (n2.lower() in n1.lower()):
                eh_duplicata = True
            elif any(k in n1.lower() for k in ['desconhecido', 'rancho']) and any(k in n2.lower() for k in ['desconhecido', 'rancho']):
                eh_duplicata = True
                
        if eh_duplicata:
            sc1 = score_qualidade_nome(n1)
            sc2 = score_qualidade_nome(n2)
            
            # Escolhe o melhor para manter
            if sc1 >= sc2:
                manter_idx, remover_idx = i, j
                m_nome, r_nome = n1, n2
                m_id, r_id = p1.get('id'), p2.get('id')
            else:
                manter_idx, remover_idx = j, i
                m_nome, r_nome = n2, n1
                m_id, r_id = p2.get('id'), p1.get('id')
                
            indices_para_remover.add(remover_idx)
            pares_resolvidos.append((d, m_id, m_nome, r_id, r_nome))
            
    return indices_para_remover, pares_resolvidos

# Testa em moradores
gdf_mor = gpd.read_file('camadas/01_moradores_e_comunidades.geojson')
rem, resolvidos = encontrar_duplicatas_camada(gdf_mor, dist_limite=25.0)

print(f"Total moradores original: {len(gdf_mor)}")
print(f"Duplicatas a remover: {len(rem)}")
print(f"Total moradores limpo: {len(gdf_mor) - len(rem)}")
print("\nExemplos de unificações realizadas:")
for d, mid, mnome, rid, rnome in resolvidos[:15]:
    print(f"  [{d:4.1f}m] Mantém ID {mid} ('{mnome}')  <-- Remove ID {rid} ('{rnome}')")
