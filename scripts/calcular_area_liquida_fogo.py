# -*- coding: utf-8 -*-
"""
Cálculo da Área Líquida Dissolvida por Intervalo e Consolidado
"""
import geopandas as gpd
import pandas as pd

ucs = gpd.read_file("camadas/00_ucs_alvo_embaubal_souzel.geojson").to_crs(epsg=31982)
revis_poly = ucs[ucs['Nome'].str.contains('Embaubal', case=False)].geometry.iloc[0]
rds_poly = ucs[ucs['Nome'].str.contains('Vit', case=False)].geometry.iloc[0]

buf = gpd.read_file("camadas/mapbiomas-fogo/Buffer_Externo_2km_UCs.shp").to_crs(epsg=31982)
buf_poly = buf.geometry.iloc[0]

# Carrega todas as cicatrizes das UCs (12_area_queimada.geojson)
aq = gpd.read_file("camadas/12_area_queimada.geojson").to_crs(epsg=31982)

# Carrega todas as cicatrizes do buffer (mapbiomas-fogo/*.shp)
import glob, os, re
files = glob.glob("camadas/mapbiomas-fogo/*.shp")
buf_gdfs = []
for f in files:
    m = re.search(r'(\d{4})', os.path.basename(f))
    if m:
        yr = int(m.group(1))
        g = gpd.read_file(f).to_crs(epsg=31982)
        if len(g) > 0:
            g['ano'] = yr
            buf_gdfs.append(g)

gdf_buf_all = pd.concat(buf_gdfs, ignore_index=True)

INTERVALOS = [
    ("1985 – 1994", 1985, 1994),
    ("1995 – 2004", 1995, 2004),
    ("2005 – 2014", 2005, 2014),
    ("2015 – 2024", 2015, 2024),
]

resultados = []
for nome_int, y0, y1 in INTERVALOS:
    # UCs sub
    sub_aq = aq[(aq['ano'] >= y0) & (aq['ano'] <= y1)]
    if len(sub_aq) > 0:
        geom_ucs_int = sub_aq.geometry.union_all()
        rev_liq = geom_ucs_int.intersection(revis_poly).area / 10000.0
        rds_liq = geom_ucs_int.intersection(rds_poly).area / 10000.0
    else:
        rev_liq, rds_liq = 0.0, 0.0

    # Buffer sub
    sub_buf = gdf_buf_all[(gdf_buf_all['ano'] >= y0) & (gdf_buf_all['ano'] <= y1)]
    if len(sub_buf) > 0:
        geom_buf_int = sub_buf.geometry.union_all()
        buf_liq = geom_buf_int.intersection(buf_poly).area / 10000.0
    else:
        buf_liq = 0.0

    tot_liq = rev_liq + rds_liq + buf_liq

    resultados.append({
        'Intervalo': nome_int,
        'REVIS_ha': round(rev_liq, 2),
        'RDS_ha': round(rds_liq, 2),
        'UCs_Total_ha': round(rev_liq + rds_liq, 2),
        'Buffer_ha': round(buf_liq, 2),
        'Total_Territorio_ha': round(tot_liq, 2),
        'Pct_Buffer': round((buf_liq / tot_liq) * 100.0, 1) if tot_liq > 0 else 0,
        'Pct_RDS': round((rds_liq / tot_liq) * 100.0, 1) if tot_liq > 0 else 0,
        'Pct_REVIS': round((rev_liq / tot_liq) * 100.0, 1) if tot_liq > 0 else 0
    })

df_res_liq = pd.DataFrame(resultados)
print("=== ÁREA LÍQUIDA DISSOLVIDA POR INTERVALO DECADAL (ha) ===")
print(df_res_liq.to_string(index=False))

# Consolidado 1985-2024
sub_aq_tot = aq[(aq['ano'] >= 1985) & (aq['ano'] <= 2024)]
geom_ucs_tot = sub_aq_tot.geometry.union_all()
rev_tot_liq = geom_ucs_tot.intersection(revis_poly).area / 10000.0
rds_tot_liq = geom_ucs_tot.intersection(rds_poly).area / 10000.0

sub_buf_tot = gdf_buf_all[(gdf_buf_all['ano'] >= 1985) & (gdf_buf_all['ano'] <= 2024)]
geom_buf_tot = sub_buf_tot.geometry.union_all()
buf_tot_liq = geom_buf_tot.intersection(buf_poly).area / 10000.0

tot_geral_liq = rev_tot_liq + rds_tot_liq + buf_tot_liq
print("\n=== CONSOLIDADO 1985–2024 LÍQUIDO DISSOLVIDO ===")
print(f"REVIS:   {rev_tot_liq:,.2f} ha ({(rev_tot_liq/4035.71)*100:.2f}% da UC)")
print(f"RDS:     {rds_tot_liq:,.2f} ha ({(rds_tot_liq/22987.41)*100:.2f}% da UC)")
print(f"UCS TOT: {rev_tot_liq + rds_tot_liq:,.2f} ha")
print(f"BUFFER:  {buf_tot_liq:,.2f} ha ({(buf_tot_liq/17117.4)*100:.2f}% do buffer)")
print(f"TOTAL:   {tot_geral_liq:,.2f} ha")
