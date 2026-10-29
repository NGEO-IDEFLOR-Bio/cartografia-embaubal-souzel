# -*- coding: utf-8 -*-
"""
Cálculo Completo e Integrado de Queimadas:
- DENTRO DAS UCs: camadas/12_area_queimada.geojson (cruzado com poligonais de REVIS e RDS)
- NO ENTORNO (BUFFER 2KM): camadas/mapbiomas-fogo/*.shp (cruzado com o Buffer_Externo)
"""

import geopandas as gpd
import pandas as pd
import glob, os, re

ucs = gpd.read_file("camadas/00_ucs_alvo_embaubal_souzel.geojson").to_crs(epsg=31982)
revis_poly = ucs[ucs['Nome'].str.contains('Embaubal', case=False)].geometry.iloc[0]
rds_poly = ucs[ucs['Nome'].str.contains('Vit', case=False)].geometry.iloc[0]

buf = gpd.read_file("camadas/mapbiomas-fogo/Buffer_Externo_2km_UCs.shp").to_crs(epsg=31982)
buf_poly = buf.geometry.iloc[0]

# 1. Fogo dentro das UCs (12_area_queimada.geojson)
aq = gpd.read_file("camadas/12_area_queimada.geojson").to_crs(epsg=31982)

# 2. Fogo no buffer (mapbiomas-fogo/*.shp)
files = glob.glob("camadas/mapbiomas-fogo/*.shp")
buf_files = {}
for f in files:
    m = re.search(r'(\d{4})', os.path.basename(f))
    if m:
        buf_files[int(m.group(1))] = f

todos_anos = sorted(set(list(aq['ano'].unique()) + list(buf_files.keys())))

registros = []
for yr in todos_anos:
    # Fogo UCs
    sub_aq = aq[aq['ano'] == yr]
    if len(sub_aq) > 0:
        geom_ucs = sub_aq.geometry.union_all()
        revis_ha = geom_ucs.intersection(revis_poly).area / 10000.0
        rds_ha = geom_ucs.intersection(rds_poly).area / 10000.0
    else:
        revis_ha, rds_ha = 0.0, 0.0

    # Fogo Buffer
    if yr in buf_files:
        gdf_b = gpd.read_file(buf_files[yr]).to_crs(epsg=31982)
        if len(gdf_b) > 0:
            geom_b = gdf_b.geometry.union_all()
            buffer_ha = geom_b.intersection(buf_poly).area / 10000.0
        else:
            buffer_ha = 0.0
    else:
        buffer_ha = 0.0

    total_ha = revis_ha + rds_ha + buffer_ha

    if 1985 <= yr <= 1994:
        intervalo = "1985 – 1994"
    elif 1995 <= yr <= 2004:
        intervalo = "1995 – 2004"
    elif 2005 <= yr <= 2014:
        intervalo = "2005 – 2014"
    elif 2015 <= yr <= 2024:
        intervalo = "2015 – 2024"
    else:
        intervalo = "2025 – 2026"

    registros.append({
        'ano': yr,
        'intervalo': intervalo,
        'revis_ha': revis_ha,
        'rds_ha': rds_ha,
        'ucs_total_ha': revis_ha + rds_ha,
        'buffer_ha': buffer_ha,
        'total_territorio_ha': total_ha
    })

df_completo = pd.DataFrame(registros)

print("=== TABELA ANUAL COMPLETA (FOGO REAL) ===")
print(df_completo.to_string(index=False))

print("\n=== RESUMO POR INTERVALO DECADAL (Soma anual) ===")
res_intervalo = df_completo.groupby('intervalo')[['revis_ha', 'rds_ha', 'ucs_total_ha', 'buffer_ha', 'total_territorio_ha']].sum()
print(res_intervalo.to_string())
