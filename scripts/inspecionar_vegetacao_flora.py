import geopandas as gpd

gdf = gpd.read_file('camadas/08_vegetacao_e_flora.geojson')
print(f"Total features in 08_vegetacao_e_flora: {len(gdf)}")
print(f"Columns: {list(gdf.columns)}")

for i, r in gdf.iterrows():
    nid = r.get('id')
    nome = r.get('nome')
    sub = r.get('subcategoria')
    obs = r.get('observacoes')
    alt = r.get('nome_alternativo')
    print(f"{i+1:2d}: ID {nid} | nome: '{nome}' | sub: '{sub}' | alt: '{alt}' | obs: '{obs}'")
