# -*- coding: utf-8 -*-
"""
Processamento Completo e Definitivo do MapBiomas Fogo (1985 - 2026)
Integra:
1. Cicatrizes DENTRO das UCs (camadas/12_area_queimada.geojson)
2. Cicatrizes no ENTORNO EXTERNO (camadas/mapbiomas-fogo/*.shp)

Cruza com poligonais exatas:
- REVIS Tabuleiro do Embaubal (4.035,71 ha)
- RDS Vitória de Souzel (22.987,41 ha)
- Zona de Amortecimento / Buffer 2km (17.117,40 ha)
"""

import os
import glob
import re
import geopandas as gpd
import pandas as pd

DIR_FOGO = "camadas/mapbiomas-fogo"
DIR_AGRUPADO = "camadas/mapbiomas-fogo/agrupado"
DIR_TABELAS = "camadas/tabelas"

os.makedirs(DIR_AGRUPADO, exist_ok=True)
os.makedirs(DIR_TABELAS, exist_ok=True)

# 1. Carrega limites legais
ucs = gpd.read_file("camadas/00_ucs_alvo_embaubal_souzel.geojson").to_crs(epsg=4674)
buf = gpd.read_file("camadas/mapbiomas-fogo/Buffer_Externo_2km_UCs.shp").to_crs(epsg=4674)

revis_geom = ucs[ucs['Nome'].str.contains('Embaubal', case=False)].geometry.iloc[0]
rds_geom = ucs[ucs['Nome'].str.contains('Vit', case=False)].geometry.iloc[0]
buf_geom = buf.geometry.iloc[0]

crs_utm = "EPSG:31982"
revis_utm = gpd.GeoSeries([revis_geom], crs="EPSG:4674").to_crs(crs_utm).iloc[0]
rds_utm = gpd.GeoSeries([rds_geom], crs="EPSG:4674").to_crs(crs_utm).iloc[0]
buf_utm = gpd.GeoSeries([buf_geom], crs="EPSG:4674").to_crs(crs_utm).iloc[0]

area_revis_total = revis_utm.area / 10000.0
area_rds_total = rds_utm.area / 10000.0
area_buf_total = buf_utm.area / 10000.0

print(f"Limites carregados: REVIS={area_revis_total:,.1f} ha, RDS={area_rds_total:,.1f} ha, Buffer={area_buf_total:,.1f} ha")

# 2. Carrega fogo UCs
gdf_ucs_fire = gpd.read_file("camadas/12_area_queimada.geojson").to_crs(epsg=4674)
gdf_ucs_fire_utm = gdf_ucs_fire.to_crs(crs_utm)

# 3. Carrega fogo Buffer
buf_files = glob.glob(f"{DIR_FOGO}/*.shp")
buf_gdfs = []
for f in buf_files:
    m = re.search(r'(\d{4})', os.path.basename(f))
    if m:
        yr = int(m.group(1))
        try:
            g = gpd.read_file(f)
            if len(g) > 0:
                g = g.to_crs(epsg=4674)
                g['ano'] = yr
                buf_gdfs.append(g)
        except Exception as e:
            print(f"Erro em {f}: {e}")

gdf_buf_fire = pd.concat(buf_gdfs, ignore_index=True)
gdf_buf_fire_utm = gdf_buf_fire.to_crs(crs_utm)

# 4. Unifica polígonos com atributos padronizados
todos_poligonos = []

# Processa cicatrizes das UCs
for idx, row in gdf_ucs_fire.iterrows():
    yr = int(row['ano'])
    geom_utm = gdf_ucs_fire_utm.loc[idx, 'geometry']
    ha_poly = geom_utm.area / 10000.0
    
    # Classifica localização precisa
    int_rev = geom_utm.intersection(revis_utm).area
    int_rds = geom_utm.intersection(rds_utm).area
    
    if int_rev > int_rds:
        loc = "REVIS Tabuleiro do Embaubal"
    else:
        loc = "RDS Vitória de Souzel"

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

    todos_poligonos.append({
        'ano': yr,
        'intervalo': intervalo,
        'area_ha': round(ha_poly, 4),
        'localidade': loc,
        'origem': 'UCs',
        'geometry': row['geometry']
    })

# Processa cicatrizes do Buffer
for idx, row in gdf_buf_fire.iterrows():
    yr = int(row['ano'])
    geom_utm = gdf_buf_fire_utm.loc[idx, 'geometry']
    ha_poly = geom_utm.area / 10000.0
    
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

    todos_poligonos.append({
        'ano': yr,
        'intervalo': intervalo,
        'area_ha': round(ha_poly, 4),
        'localidade': 'Zona de Amortecimento (Buffer 2km)',
        'origem': 'Buffer',
        'geometry': row['geometry']
    })

gdf_todos = gpd.GeoDataFrame(todos_poligonos, crs="EPSG:4674")
print(f"Total de cicatrizes consolidadas: {len(gdf_todos)} polígonos")

# Salva shapefile e geopackage completo
gdf_todos.to_file(f"{DIR_AGRUPADO}/mapbiomas_fogo_1985_2026_consolidado.shp", encoding="utf-8")
gdf_todos.to_file(f"{DIR_AGRUPADO}/mapbiomas_fogo_1985_2026_consolidado.gpkg", layer="cicatrizes_fogo", driver="GPKG")

# 5. Salva camadas agrupadas por intervalo decadal
INTERVALOS = [
    ("1985_1994", "1985 – 1994", 1985, 1994),
    ("1995_2004", "1995 – 2004", 1995, 2004),
    ("2005_2014", "2005 – 2014", 2005, 2014),
    ("2015_2024", "2015 – 2024", 2015, 2024),
]

stats_intervalos = []

for suf, nome_int, y0, y1 in INTERVALOS:
    sub_gdf = gdf_todos[gdf_todos['intervalo'] == nome_int]
    
    sub_gdf.to_file(f"{DIR_AGRUPADO}/fogo_{suf}.shp", encoding="utf-8")
    sub_gdf.to_file(f"{DIR_AGRUPADO}/fogo_{suf}.gpkg", layer=f"fogo_{suf}", driver="GPKG")

    # Cálculo da área líquida sem dupla contagem (dissolve geométrico no intervalo)
    sub_utm = sub_gdf.to_crs(crs_utm)
    sub_rev = sub_utm[sub_utm['localidade'] == "REVIS Tabuleiro do Embaubal"]
    sub_rds = sub_utm[sub_utm['localidade'] == "RDS Vitória de Souzel"]
    sub_buf = sub_utm[sub_utm['localidade'] == "Zona de Amortecimento (Buffer 2km)"]

    rev_liq = sub_rev.geometry.union_all().intersection(revis_utm).area / 10000.0 if len(sub_rev) > 0 else 0.0
    rds_liq = sub_rds.geometry.union_all().intersection(rds_utm).area / 10000.0 if len(sub_rds) > 0 else 0.0
    buf_liq = sub_buf.geometry.union_all().intersection(buf_utm).area / 10000.0 if len(sub_buf) > 0 else 0.0

    tot_liq = rev_liq + rds_liq + buf_liq

    stats_intervalos.append({
        'Intervalo': nome_int,
        'Qtd_Cicatrizes': len(sub_gdf),
        'REVIS_ha': round(rev_liq, 2),
        'RDS_ha': round(rds_liq, 2),
        'UCs_Total_ha': round(rev_liq + rds_liq, 2),
        'Buffer_ha': round(buf_liq, 2),
        'Total_ha': round(tot_liq, 2),
        'Pct_Buffer': round((buf_liq / tot_liq) * 100.0, 1) if tot_liq > 0 else 0,
        'Pct_RDS': round((rds_liq / tot_liq) * 100.0, 1) if tot_liq > 0 else 0,
        'Pct_REVIS': round((rev_liq / tot_liq) * 100.0, 1) if tot_liq > 0 else 0
    })
    print(f"[{nome_int}] Total: {tot_liq:,.1f} ha | RDS: {rds_liq:,.1f} ha | Buffer: {buf_liq:,.1f} ha | REVIS: {rev_liq:,.1f} ha")

df_int = pd.DataFrame(stats_intervalos)
df_int.to_csv(f"{DIR_TABELAS}/estatisticas_mapbiomas_fogo_intervalos.csv", index=False)
print(f"[OK] Tabela por intervalos salva em {DIR_TABELAS}/estatisticas_mapbiomas_fogo_intervalos.csv")

# 6. Salva série histórica anual completa
anos_unicos = sorted(gdf_todos['ano'].unique())
stats_anuais = []
for yr in anos_unicos:
    sub_yr = gdf_todos[gdf_todos['ano'] == yr].to_crs(crs_utm)
    sub_rev = sub_yr[sub_yr['localidade'] == "REVIS Tabuleiro do Embaubal"]
    sub_rds = sub_yr[sub_yr['localidade'] == "RDS Vitória de Souzel"]
    sub_buf = sub_yr[sub_yr['localidade'] == "Zona de Amortecimento (Buffer 2km)"]

    rev_ha = sub_rev.geometry.union_all().intersection(revis_utm).area / 10000.0 if len(sub_rev) > 0 else 0.0
    rds_ha = sub_rds.geometry.union_all().intersection(rds_utm).area / 10000.0 if len(sub_rds) > 0 else 0.0
    buf_ha = sub_buf.geometry.union_all().intersection(buf_utm).area / 10000.0 if len(sub_buf) > 0 else 0.0

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

    stats_anuais.append({
        'ano': yr,
        'intervalo': intervalo,
        'qtd_poligonos': len(sub_yr),
        'ha_revis': round(rev_ha, 2),
        'ha_rds': round(rds_ha, 2),
        'ha_ucs_total': round(rev_ha + rds_ha, 2),
        'ha_buffer': round(buf_ha, 2),
        'ha_total': round(rev_ha + rds_ha + buf_ha, 2)
    })

df_anual = pd.DataFrame(stats_anuais)
df_anual.to_csv(f"{DIR_TABELAS}/estatisticas_anuais_mapbiomas_fogo_1985_2026.csv", index=False)
print(f"[OK] Estatísticas anuais salvas em {DIR_TABELAS}/estatisticas_anuais_mapbiomas_fogo_1985_2026.csv")
