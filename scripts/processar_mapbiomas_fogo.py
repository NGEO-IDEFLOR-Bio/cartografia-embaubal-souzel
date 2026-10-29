# -*- coding: utf-8 -*-
"""
Processamento e Agrupamento Temporal - MapBiomas Fogo (1985 - 2026)
Área de Estudo: REVIS Tabuleiro do Embaubal, RDS Vitória de Souzel e Buffer de 2km.

Gera:
1. Camadas vetoriais agrupadas por intervalo temporal (1985-1994, 1995-2004, 2005-2014, 2015-2024 e Consolidado).
2. Tabela de estatísticas zonais consolidadas (CSV) em hectares e percentuais.
3. Classificação territorial de cada cicatriz (REVIS, RDS ou Entorno / Buffer 2km).
"""

import os
import glob
import re
import json
import geopandas as gpd
import pandas as pd
from shapely.ops import unary_union

DIR_FOGO = "camadas/mapbiomas-fogo"
DIR_AGRUPADO = "camadas/mapbiomas-fogo/agrupado"
DIR_TABELAS = "camadas/tabelas"

os.makedirs(DIR_AGRUPADO, exist_ok=True)
os.makedirs(DIR_TABELAS, exist_ok=True)

print("Carregando limites territoriais...")
ucs = gpd.read_file("camadas/00_ucs_alvo_embaubal_souzel.geojson").to_crs(epsg=4674)
buf = gpd.read_file("camadas/mapbiomas-fogo/Buffer_Externo_2km_UCs.shp").to_crs(epsg=4674)

revis_geom = ucs[ucs['Nome'].str.contains('Embaubal', case=False)].geometry.iloc[0]
rds_geom = ucs[ucs['Nome'].str.contains('Vit', case=False)].geometry.iloc[0]
buf_geom = buf.geometry.iloc[0]

# Projeta para UTM 22S para cálculo métrico de área
crs_utm = "EPSG:31982"
revis_utm = gpd.GeoSeries([revis_geom], crs="EPSG:4674").to_crs(crs_utm).iloc[0]
rds_utm = gpd.GeoSeries([rds_geom], crs="EPSG:4674").to_crs(crs_utm).iloc[0]
buf_utm = gpd.GeoSeries([buf_geom], crs="EPSG:4674").to_crs(crs_utm).iloc[0]

area_revis_total = revis_utm.area / 10000.0
area_rds_total = rds_utm.area / 10000.0
area_buf_total = buf_utm.area / 10000.0

print(f"Área REVIS: {area_revis_total:.2f} ha")
print(f"Área RDS:   {area_rds_total:.2f} ha")
print(f"Área Buffer:{area_buf_total:.2f} ha")

# Identifica todos os shapefiles anuais
files = glob.glob(f"{DIR_FOGO}/*.shp")
file_years = []
for f in files:
    m = re.search(r'(\d{4})', os.path.basename(f))
    if m:
        yr = int(m.group(1))
        file_years.append((yr, f))
file_years.sort()

print(f"Total de safras anuais encontradas: {len(file_years)} anos")

# Estrutura para consolidar polígonos
todos_poligonos = []
stats_anuais = []

for yr, fpath in file_years:
    try:
        gdf_yr = gpd.read_file(fpath)
        if len(gdf_yr) == 0:
            stats_anuais.append({
                'ano': yr, 'intervalo': '', 'qtd_poligonos': 0,
                'ha_revis': 0.0, 'ha_rds': 0.0, 'ha_buffer': 0.0, 'ha_total': 0.0
            })
            continue

        gdf_yr = gdf_yr.to_crs(epsg=4674)
        gdf_yr_utm = gdf_yr.to_crs(crs_utm)

        # Determina o intervalo decadal padrão MapBiomas
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

        # Calcula áreas por unidade usando UTM
        # Dissolve anual para métricas agregadas sem duplicidade de sobreposição
        union_geom_utm = gdf_yr_utm.geometry.union_all()
        
        ha_rev = union_geom_utm.intersection(revis_utm).area / 10000.0
        ha_rds = union_geom_utm.intersection(rds_utm).area / 10000.0
        ha_buf = union_geom_utm.intersection(buf_utm).area / 10000.0
        ha_tot = union_geom_utm.area / 10000.0

        stats_anuais.append({
            'ano': yr,
            'intervalo': intervalo,
            'qtd_poligonos': len(gdf_yr),
            'ha_revis': ha_rev,
            'ha_rds': ha_rds,
            'ha_buffer': ha_buf,
            'ha_total': ha_tot
        })

        # Prepara features padronizadas com atributos uniformes
        for idx, row in gdf_yr.iterrows():
            geom_utm = gdf_yr_utm.loc[idx, 'geometry']
            ha_poly = geom_utm.area / 10000.0
            
            # Identifica localização predominante do polígono
            int_rev = geom_utm.intersection(revis_utm).area
            int_rds = geom_utm.intersection(rds_utm).area
            int_buf = geom_utm.intersection(buf_utm).area
            
            if int_rev > int_rds and int_rev > int_buf:
                loc = "REVIS Tabuleiro do Embaubal"
            elif int_rds > int_rev and int_rds > int_buf:
                loc = "RDS Vitória de Souzel"
            else:
                loc = "Zona de Amortecimento (Buffer 2km)"

            todos_poligonos.append({
                'ano': yr,
                'intervalo': intervalo,
                'area_ha': round(ha_poly, 4),
                'localidade': loc,
                'geometry': row['geometry']
            })

    except Exception as e:
        print(f"Erro ao processar {yr}: {e}")

df_stats = pd.DataFrame(stats_anuais)
df_stats.to_csv(f"{DIR_TABELAS}/estatisticas_anuais_mapbiomas_fogo_1985_2026.csv", index=False)
print(f"[OK] Estatísticas anuais salvas em {DIR_TABELAS}/estatisticas_anuais_mapbiomas_fogo_1985_2026.csv")

# Cria GeoDataFrame consolidado
gdf_todos = gpd.GeoDataFrame(todos_poligonos, crs="EPSG:4674")

# Salva camada consolidada em Shapefile e GeoPackage
gdf_todos.to_file(f"{DIR_AGRUPADO}/mapbiomas_fogo_1985_2026_consolidado.shp", encoding="utf-8")
gdf_todos.to_file(f"{DIR_AGRUPADO}/mapbiomas_fogo_1985_2026_consolidado.gpkg", layer="cicatrizes_fogo", driver="GPKG")
print("[OK] Camada consolidada salva em GeoPackage e Shapefile.")

# Salva camadas agrupadas por intervalo decadal
INTERVALOS = [
    ("1985_1994", "1985 – 1994"),
    ("1995_2004", "1995 – 2004"),
    ("2005_2014", "2005 – 2014"),
    ("2015_2024", "2015 – 2024"),
]

stats_intervalos = []

for suf, nome_int in INTERVALOS:
    sub_gdf = gdf_todos[gdf_todos['intervalo'] == nome_int]
    
    # Salva arquivos vetoriais do intervalo
    shp_path = f"{DIR_AGRUPADO}/fogo_{suf}.shp"
    gpkg_path = f"{DIR_AGRUPADO}/fogo_{suf}.gpkg"
    sub_gdf.to_file(shp_path, encoding="utf-8")
    sub_gdf.to_file(gpkg_path, layer=f"fogo_{suf}", driver="GPKG")
    
    # Agregação estatística sem dupla contagem (dissolve de polígonos no intervalo)
    sub_utm = sub_gdf.to_crs(crs_utm)
    if len(sub_utm) > 0:
        union_int_utm = sub_utm.geometry.union_all()
        ha_rev = union_int_utm.intersection(revis_utm).area / 10000.0
        ha_rds = union_int_utm.intersection(rds_utm).area / 10000.0
        ha_buf = union_int_utm.intersection(buf_utm).area / 10000.0
        ha_tot = union_int_utm.area / 10000.0
    else:
        ha_rev, ha_rds, ha_buf, ha_tot = 0.0, 0.0, 0.0, 0.0

    stats_intervalos.append({
        'Intervalo': nome_int,
        'Qtd_Cicatrizes': len(sub_gdf),
        'REVIS_ha': round(ha_rev, 2),
        'RDS_ha': round(ha_rds, 2),
        'Buffer_ha': round(ha_buf, 2),
        'Total_ha': round(ha_tot, 2),
        'Pct_Buffer': round((ha_buf / area_buf_total) * 100.0, 2),
        'Pct_RDS': round((ha_rds / area_rds_total) * 100.0, 4),
        'Pct_REVIS': round((ha_rev / area_revis_total) * 100.0, 4)
    })
    print(f"[OK] Intervalo {nome_int}: {len(sub_gdf)} cicatrizes, Total {ha_tot:.2f} ha (Buffer: {ha_buf:.2f} ha, RDS: {ha_rds:.2f} ha, REVIS: {ha_rev:.2f} ha)")

df_int = pd.DataFrame(stats_intervalos)
df_int.to_csv(f"{DIR_TABELAS}/estatisticas_mapbiomas_fogo_intervalos.csv", index=False)
print(f"[OK] Tabela por intervalos salva em {DIR_TABELAS}/estatisticas_mapbiomas_fogo_intervalos.csv")
