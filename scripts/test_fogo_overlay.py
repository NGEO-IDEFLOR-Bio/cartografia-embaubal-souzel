import geopandas as gpd

ucs = gpd.read_file("camadas/00_ucs_alvo_embaubal_souzel.geojson")
print("UCs CRS:", ucs.crs)
print("UCs bounds:", ucs.total_bounds)
for idx, r in ucs.iterrows():
    print(f"UC {idx}: {r['Nome']} -> bounds: {r.geometry.bounds}")

fogo_2023 = gpd.read_file("camadas/mapbiomas-fogo/Fogo_Buffer_2km_2023.shp")
print("Fogo 2023 CRS:", fogo_2023.crs)
print("Fogo 2023 bounds:", fogo_2023.total_bounds)

buf = gpd.read_file("camadas/mapbiomas-fogo/Buffer_Externo_2km_UCs.shp")
print("Buffer CRS:", buf.crs)
print("Buffer bounds:", buf.total_bounds)

# Now check spatial intersection between Fogo 2023 and UCs directly
# Check if any geometry intersects
print("\nChecking intersection between Fogo 2023 and UCs:")
revis = ucs[ucs['Nome'].str.contains('Embaubal', case=False)].geometry.iloc[0]
rds = ucs[ucs['Nome'].str.contains('Vit', case=False)].geometry.iloc[0]

int_revis = fogo_2023[fogo_2023.intersects(revis)]
print(f"Fogo 2023 intersecting REVIS: {len(int_revis)} features")

int_rds = fogo_2023[fogo_2023.intersects(rds)]
print(f"Fogo 2023 intersecting RDS: {len(int_rds)} features")

int_buf = fogo_2023[fogo_2023.intersects(buf.geometry.iloc[0])]
print(f"Fogo 2023 intersecting Buffer: {len(int_buf)} features")
