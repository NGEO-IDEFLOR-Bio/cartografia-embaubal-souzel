# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd

ucs = gpd.read_file("camadas/00_ucs_alvo_embaubal_souzel.geojson").to_crs(epsg=31982)
revis_poly = ucs[ucs['Nome'].str.contains('Embaubal', case=False)].geometry.iloc[0]
rds_poly = ucs[ucs['Nome'].str.contains('Vit', case=False)].geometry.iloc[0]

aq = gpd.read_file("camadas/12_area_queimada.geojson").to_crs(epsg=31982)

# Interseção precisa com REVIS e RDS
records = []
for yr in sorted(aq['ano'].unique()):
    sub_yr = aq[aq['ano'] == yr]
    geom_yr = sub_yr.geometry.union_all()
    
    rev_ha = geom_yr.intersection(revis_poly).area / 10000.0
    rds_ha = geom_yr.intersection(rds_poly).area / 10000.0
    
    records.append({
        'ano': int(yr),
        'revis_ha': rev_ha,
        'rds_ha': rds_ha,
        'total_ucs_ha': rev_ha + rds_ha
    })

df_int_ucs = pd.DataFrame(records)
print("=== FOGO DENTRO DAS UNIDADES (12_area_queimada) ===")
print(df_int_ucs.to_string(index=False))

print(f"\nTOTAL ACUMULADO DENTRO DAS UCS:")
print(f"REVIS: {df_int_ucs.revis_ha.sum():,.2f} ha")
print(f"RDS:   {df_int_ucs.rds_ha.sum():,.2f} ha")
print(f"TOTAL: {df_int_ucs.total_ucs_ha.sum():,.2f} ha")
