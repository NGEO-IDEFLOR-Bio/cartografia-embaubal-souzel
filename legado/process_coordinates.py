import openpyxl
import re
import json
import os
import math
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Ensure output directories exist
os.makedirs("dados_organizados", exist_ok=True)
os.makedirs("dados_organizados/camadas_tematicas", exist_ok=True)

wb1 = openpyxl.load_workbook("Coordenadas.1.xlsx", data_only=True)
wb2 = openpyxl.load_workbook("Coordenadas.2.xlsx", data_only=True)

# 1. Legend from wb2 COORD. GERAL cols 5-7 (Mapping numbers 1..88)
legend = {}
ws2_gen = wb2["COORD. GERAL"]
for r in range(2, 75):
    num = ws2_gen.cell(r, 5).value
    desc = ws2_gen.cell(r, 6).value
    if num is not None and desc:
        legend[str(num).strip()] = str(desc).strip()

def parse_coord(val):
    if not val:
        return None
    s = str(val).strip().replace(";", ",")
    parts = s.split(",")
    if len(parts) == 2:
        try:
            return round(float(parts[0]), 6), round(float(parts[1]), 6)
        except:
            return None
    return None

def extract_date_and_clean_name(name_raw):
    name = str(name_raw).strip()
    date_val = None
    # Pattern: -Wpt 22/10/2025, 12:32:46 or Wpt 22/10/2025, 12:32:46
    m = re.search(r'[-–]?\s*Wpt\s*(\d{2}/\d{2}/\d{4},\s*\d{2}:\d{2}:\d{2})', name, re.IGNORECASE)
    if m:
        date_val = m.group(1)
        name = re.sub(r'[-–]?\s*Wpt\s*\d{2}/\d{2}/\d{4},\s*\d{2}:\d{2}:\d{2}', '', name, flags=re.IGNORECASE).strip()
    else:
        m2 = re.search(r'[-–]?\s*(\d{2}/\d{2}/\d{4},\s*\d{2}:\d{2}:\d{2})', name)
        if m2:
            date_val = m2.group(1)
            name = re.sub(r'[-–]?\s*\d{2}/\d{2}/\d{4},\s*\d{2}:\d{2}:\d{2}', '', name).strip()
    
    # Strip leading / trailing dashes or punctuation
    name = re.sub(r'^[–\-\s]+|[–\-\s]+$', '', name)
    return name, date_val

# 2. Known duplicates from wb2 DUPLICADAS (Kelly vs Lorena)
known_dups = {}
ws_dup = wb2["DUPLICADAS"]
for r in ws_dup.iter_rows(values_only=True):
    if r and r[0] and r[0] != "Nomeclatura - Kelly":
        k_name = str(r[0]).strip()
        k_coord = parse_coord(r[1])
        l_name = str(r[2]).strip()
        l_coord = parse_coord(r[3])
        dist = str(r[4]).strip() if len(r) > 4 else ""
        known_dups[k_name] = {
            "k_coord": k_coord,
            "l_name": l_name,
            "l_coord": l_coord,
            "dist": dist
        }

def in_uc_region(lat, lon):
    return -3.05 <= lat <= -2.55 and -52.25 <= lon <= -51.80

# 3. Categorization Helper
def classify_point(name, sheet_origin, code_orig=None):
    s = (sheet_origin or "").strip().upper()
    n = name.lower()
    
    cat = "Marcos e Pontos de Referência"
    subcat = "Geral"
    
    # Priority by sheet
    if s in ["MORADORES", " MORADORES"]:
        cat = "Moradores e Comunidades"
        subcat = "Residência Ribeirinha"
    elif s in ["APOIO DE PESCA - PESCA"]:
        cat = "Apoio de Pesca e Ranchos"
        subcat = "Ponto de Apoio / Pesqueiro"
    elif s in ["DESOVA", "DESOVA-PESCA"]:
        cat = "Áreas de Desova"
        if "peixe" in n or "curimat" in n:
            subcat = "Desova de Peixes"
        else:
            subcat = "Desova de Quelônios (Tartaruga/Tracajá/Pitiú)"
    elif s in ["FURO", "FUROS"]:
        cat = "Hidrografia"
        subcat = "Furos"
    elif s in ["IGARAPE", "IGARAPES"]:
        cat = "Hidrografia"
        subcat = "Igarapés"
    elif s in ["RIOS"]:
        cat = "Hidrografia"
        subcat = "Rios"
    elif s in ["LAGOS"]:
        cat = "Hidrografia"
        subcat = "Lagos"
    elif s in ["POÇOS", "POOS"]:
        cat = "Infraestrutura e Equipamentos Públicos"
        subcat = "Poços"
    elif s in ["ILHAS"]:
        cat = "Ilhas e Praias"
        subcat = "Ilhas"
    elif s in ["PRAIA - BANCO DE AREIA"]:
        cat = "Ilhas e Praias"
        subcat = "Praias e Bancos de Areia"
    elif s in ["PUSADAS-PRAIAS"]:
        if "pousada" in n:
            cat = "Infraestrutura e Turismo"
            subcat = "Pousadas"
        else:
            cat = "Ilhas e Praias"
            subcat = "Praias e Bancos de Areia"
    elif s in ["CONSTRUÇÃO", "CONSTRUO", "PONTS. ESTRATEGICOS"]:
        cat = "Infraestrutura e Equipamentos Públicos"
        if "base" in n:
            subcat = "Bases Institucionais"
        elif "igreja" in n:
            subcat = "Igrejas / Templos"
        elif "escola" in n:
            subcat = "Escolas"
        else:
            subcat = "Estruturas e Equipamentos"
    elif s in ["VEGETAÇÃO - NATURAZA", "VEGETAO - NATURAZA"]:
        cat = "Vegetação e Flora"
        subcat = "Flora / Recursos Naturais"
    elif s in ["FOGO - INCENDIOS"]:
        cat = "Ocorrências e Impactos"
        subcat = "Cicatriz de Fogo / Incêndio"
    elif s in ["TRAJETOS"]:
        cat = "Trajetos e Acessos"
        subcat = "Trajetos e Monitoramento"
    elif s in ["PONTOS DE REFERENCIA"]:
        cat = "Marcos e Pontos de Referência"
        subcat = "Referência Local"
    else:
        # Fallback from name
        if any(w in n for w in ["desova", "tartaruga", "tracaj", "curimat"]):
            cat = "Áreas de Desova"
            subcat = "Desova de Peixes" if "curimat" in n else "Desova de Quelônios"
        elif "furo" in n:
            cat = "Hidrografia"
            subcat = "Furos"
        elif "igarap" in n or n.startswith("ig."):
            cat = "Hidrografia"
            subcat = "Igarapés"
        elif "rio" in n:
            cat = "Hidrografia"
            subcat = "Rios"
        elif "lago" in n:
            cat = "Hidrografia"
            subcat = "Lagos"
        elif "ilha" in n:
            cat = "Ilhas e Praias"
            subcat = "Ilhas"
        elif "praia" in n or "banco de areia" in n:
            cat = "Ilhas e Praias"
            subcat = "Praias e Bancos de Areia"
        elif "rancho" in n or "pesca" in n:
            cat = "Apoio de Pesca e Ranchos"
            subcat = "Ponto de Apoio / Pesqueiro"
        elif any(w in n for w in ["base", "escola", "igreja", "barrac", "posto"]):
            cat = "Infraestrutura e Equipamentos Públicos"
            subcat = "Equipamento Público / Comunitário"
        elif any(w in n for w in ["fogo", "queimada", "búfalo", "bufalo", "abertura de canal"]):
            cat = "Ocorrências e Impactos"
            subcat = "Impacto / Ocorrência"
        elif any(w in n for w in ["seringueira", "jatob", "castanheira", "mata"]):
            cat = "Vegetação e Flora"
            subcat = "Flora / Árvore Matriz"
        else:
            cat = "Moradores e Comunidades"
            subcat = "Residência Ribeirinha"
            
    return cat, subcat

# Build a mapping of coordinates to thematic sheet in wb2
wb2_thematic_map = {}
for s in wb2.sheetnames:
    if s in ["COORD. GERAL", "DUPLICADAS"]: continue
    ws = wb2[s]
    for r in ws.iter_rows(values_only=True):
        if r and len(r) > 1 and r[0] and r[1]:
            c = parse_coord(r[1])
            if c:
                wb2_thematic_map[c] = s

# Build a mapping of coordinates to thematic sheet in wb1
wb1_thematic_map = {}
for s in wb1.sheetnames:
    if s == "COORD. GERAL": continue
    ws = wb1[s]
    for r in ws.iter_rows(values_only=True):
        if r and len(r) > 1 and r[0] and r[1]:
            c = parse_coord(r[1])
            if c:
                wb1_thematic_map[c] = s

# Collect points from wb2
all_records = []
processed_coords = set()

# Process wb2 COORD. GERAL
ws2_gen = wb2["COORD. GERAL"]
for r in range(2, ws2_gen.max_row + 1):
    raw_name = ws2_gen.cell(r, 1).value
    coord_str = ws2_gen.cell(r, 2).value
    if not raw_name and not coord_str:
        continue
    c = parse_coord(coord_str)
    if not c:
        continue
    
    # Check if raw_name is a number
    cod_orig = None
    decoded_desc = None
    name_str = str(raw_name).strip()
    if name_str in legend:
        cod_orig = int(name_str)
        decoded_desc = legend[name_str]
        # Clean decoded description
        clean_name = decoded_desc
        # Extract e.g. "Morador (Antônio - Guariba)" -> "Antônio (Guariba)"
        m = re.match(r'^(?:Morador|Localidade\s*/\s*Referência|Apoio de Pesca\s*/\s*Morador|Apoio de Pesca|Rancho\s*/\s*Estrutura abandonada)\s*\((.*?)\)$', decoded_desc, re.IGNORECASE)
        if m:
            clean_name = m.group(1).strip()
    else:
        clean_name, date_extracted = extract_date_and_clean_name(name_str)
    
    _, date_extracted = extract_date_and_clean_name(name_str)
    
    # Origin sheet
    sheet_orig = wb2_thematic_map.get(c, "COORD. GERAL")
    cat, subcat = classify_point(clean_name if not decoded_desc else decoded_desc, sheet_orig, cod_orig)
    
    # Check if this point was in DUPLICADAS (Lorena side)
    alias = None
    obs = None
    for k_n, dinfo in known_dups.items():
        if dinfo["l_coord"] == c or dinfo["l_name"].lower() == name_str.lower():
            alias = f"Kelly: {k_n}"
            obs = f"Ponto consolidado entre Kelly ({k_n}) e Lorena ({dinfo['l_name']}). Distância aprox: {dinfo['dist']}"
            break
            
    rec = {
        "nome": clean_name,
        "categoria": cat,
        "subcategoria": subcat,
        "unidade_conservacao": "REVIS Tabuleiro do Embaubal / RDS Vitória de Souzel" if in_uc_region(c[0], c[1]) else "Outra Região",
        "nome_alternativo": alias or "",
        "observacoes": obs or (decoded_desc if decoded_desc and decoded_desc != clean_name else ""),
        "data_coleta": date_extracted or "",
        "cod_original": cod_orig if cod_orig else "",
        "fonte": "Consolidado (Lorena & Kelly)" if alias else "Lorena (Coordenadas.2)",
        "latitude": c[0],
        "longitude": c[1],
        "in_uc": in_uc_region(c[0], c[1])
    }
    all_records.append(rec)
    processed_coords.add(c)

# Process wb1 COORD. GERAL (Kelly points)
ws1_gen = wb1["COORD. GERAL"]
for r in range(3, ws1_gen.max_row + 1):
    raw_name = ws1_gen.cell(r, 1).value
    coord_str = ws1_gen.cell(r, 2).value
    obs_col = ws1_gen.cell(r, 3).value
    if not raw_name and not coord_str:
        continue
    c = parse_coord(coord_str)
    if not c:
        continue
    
    # If coordinate was already added from wb2, skip or update
    if c in processed_coords:
        continue
    
    name_str = str(raw_name).strip()
    
    # Check if this name is in DUPLICADAS
    if name_str in known_dups:
        # Check if Lorena coord was added
        l_coord = known_dups[name_str]["l_coord"]
        if l_coord in processed_coords:
            continue
    
    clean_name, date_extracted = extract_date_and_clean_name(name_str)
    sheet_orig = wb1_thematic_map.get(c, "COORD. GERAL")
    cat, subcat = classify_point(clean_name, sheet_orig)
    
    rec = {
        "nome": clean_name,
        "categoria": cat,
        "subcategoria": subcat,
        "unidade_conservacao": "REVIS Tabuleiro do Embaubal / RDS Vitória de Souzel" if in_uc_region(c[0], c[1]) else "Outra Região",
        "nome_alternativo": "",
        "observacoes": str(obs_col).strip() if obs_col else "",
        "data_coleta": date_extracted or "",
        "cod_original": "",
        "fonte": "Kelly (Coordenadas.1)",
        "latitude": c[0],
        "longitude": c[1],
        "in_uc": in_uc_region(c[0], c[1])
    }
    all_records.append(rec)
    processed_coords.add(c)

# Split into UC records and Other Regions records
uc_records = [r for r in all_records if r["in_uc"]]
other_records = [r for r in all_records if not r["in_uc"]]

# Assign sequential IDs
for idx, r in enumerate(uc_records, 1):
    r["id"] = idx
for idx, r in enumerate(other_records, 1):
    r["id"] = idx

print(f"Total points inside UCs (REVIS & RDS): {len(uc_records)}")
print(f"Total points outside UCs: {len(other_records)}")

# Convert to DataFrame
df_uc = pd.DataFrame(uc_records)
df_other = pd.DataFrame(other_records)

# Create GeoDataFrame for UC
gdf_uc = gpd.GeoDataFrame(
    df_uc,
    geometry=[Point(xy) for xy in zip(df_uc["longitude"], df_uc["latitude"])],
    crs="EPSG:4326"
)

# Export consolidated GeoJSON
gdf_uc.drop(columns=["in_uc"]).to_file("dados_organizados/pontos_revis_rds_consolidado.geojson", driver="GeoJSON")
print("Saved: dados_organizados/pontos_revis_rds_consolidado.geojson")

# Export GeoPackage (GPKG) with separate thematic layers for QGIS / ArcGIS
gpkg_path = "dados_organizados/pontos_revis_rds_consolidado.gpkg"
# Save consolidated layer
gdf_uc.drop(columns=["in_uc"]).to_file(gpkg_path, layer="todos_os_pontos", driver="GPKG")

# Export separate thematic layers
thematic_groups = sorted(gdf_uc["categoria"].unique())
print(f"\nThematic groups ({len(thematic_groups)}):")
for cat in thematic_groups:
    sub_gdf = gdf_uc[gdf_uc["categoria"] == cat].drop(columns=["in_uc"])
    safe_layer_name = re.sub(r'[^a-zA-Z0-9_]', '_', cat.lower()).strip('_')
    safe_layer_name = re.sub(r'_+', '_', safe_layer_name)
    
    # Save into GeoPackage
    sub_gdf.to_file(gpkg_path, layer=safe_layer_name, driver="GPKG")
    
    # Save individual GeoJSON
    geojson_filename = f"dados_organizados/camadas_tematicas/{safe_layer_name}.geojson"
    sub_gdf.to_file(geojson_filename, driver="GeoJSON")
    print(f"  [{cat}]: {len(sub_gdf)} points -> {safe_layer_name}")

# Export Other Regions to GeoJSON
if not df_other.empty:
    gdf_other = gpd.GeoDataFrame(
        df_other,
        geometry=[Point(xy) for xy in zip(df_other["longitude"], df_other["latitude"])],
        crs="EPSG:4326"
    )
    gdf_other.drop(columns=["in_uc"]).to_file("dados_organizados/pontos_outras_regioes.geojson", driver="GeoJSON")
    print("\nSaved: dados_organizados/pontos_outras_regioes.geojson")

# Export Excel Workbook with separate sheets per theme + Consolidated sheet
with pd.ExcelWriter("dados_organizados/pontos_revis_rds_consolidado.xlsx", engine="openpyxl") as writer:
    df_uc_clean = df_uc.drop(columns=["in_uc"])
    df_uc_clean.to_excel(writer, sheet_name="GERAL CONSOLIDADO", index=False)
    for cat in thematic_groups:
        sub_df = df_uc_clean[df_uc_clean["categoria"] == cat]
        sheet_title = cat[:31] # Excel sheet limit 31 chars
        sub_df.to_excel(writer, sheet_name=sheet_title, index=False)
    if not df_other.empty:
        df_other.drop(columns=["in_uc"]).to_excel(writer, sheet_name="OUTRAS REGIOES", index=False)

print("Saved: dados_organizados/pontos_revis_rds_consolidado.xlsx")

# Generate rich KML with Folder structure and HTML Popups
def generate_kml(records, output_path, doc_title):
    kml_header = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{doc_title}</name>
    <open>1</open>
    <description>Pontos Cartográficos Consolidados - IDEFLOR-Bio (REVIS Tabuleiro do Embaubal e RDS Vitória de Souzel)</description>
"""
    # Category colors / styles
    styles = """
    <Style id="moradorStyle">
      <IconStyle>
        <color>ff00aaff</color>
        <scale>1.1</scale>
        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/homegardenbusiness.png</href></Icon>
      </IconStyle>
    </Style>
    <Style id="pescaStyle">
      <IconStyle>
        <color>ff00d7ff</color>
        <scale>1.1</scale>
        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/fishing.png</href></Icon>
      </IconStyle>
    </Style>
    <Style id="desovaStyle">
      <IconStyle>
        <color>ff00ff00</color>
        <scale>1.2</scale>
        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/caution.png</href></Icon>
      </IconStyle>
    </Style>
    <Style id="hidroStyle">
      <IconStyle>
        <color>ffffaa00</color>
        <scale>1.0</scale>
        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/water.png</href></Icon>
      </IconStyle>
    </Style>
    <Style id="ilhaStyle">
      <IconStyle>
        <color>ff00ffff</color>
        <scale>1.0</scale>
        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon>
      </IconStyle>
    </Style>
    <Style id="infraStyle">
      <IconStyle>
        <color>ff0000ff</color>
        <scale>1.2</scale>
        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/ranger_station.png</href></Icon>
      </IconStyle>
    </Style>
    <Style id="floraStyle">
      <IconStyle>
        <color>ff228b22</color>
        <scale>1.1</scale>
        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/parks.png</href></Icon>
      </IconStyle>
    </Style>
    <Style id="fogoStyle">
      <IconStyle>
        <color>ff0000ee</color>
        <scale>1.1</scale>
        <Icon><href>http://maps.google.com/mapfiles/kml/shapes/firedept.png</href></Icon>
      </IconStyle>
    </Style>
    <Style id="defaultStyle">
      <IconStyle>
        <color>ffffff00</color>
        <scale>1.0</scale>
        <Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon>
      </IconStyle>
    </Style>
"""
    style_map = {
        "Moradores e Comunidades": "#moradorStyle",
        "Apoio de Pesca e Ranchos": "#pescaStyle",
        "Áreas de Desova": "#desovaStyle",
        "Hidrografia": "#hidroStyle",
        "Ilhas e Praias": "#ilhaStyle",
        "Infraestrutura e Equipamentos Públicos": "#infraStyle",
        "Vegetação e Flora": "#floraStyle",
        "Ocorrências e Impactos": "#fogoStyle"
    }
    
    # Group by category
    cats = {}
    for r in records:
        c = r["categoria"]
        if c not in cats: cats[c] = []
        cats[c].append(r)
        
    kml_body = ""
    for cat_name, items in sorted(cats.items()):
        kml_body += f'    <Folder>\n      <name>{cat_name} ({len(items)})</name>\n      <open>0</open>\n'
        for it in items:
            s_url = style_map.get(cat_name, "#defaultStyle")
            desc_html = f"""<![CDATA[
                <h3>{it['nome']}</h3>
                <p><b>Categoria:</b> {it['categoria']}</p>
                <p><b>Subcategoria:</b> {it['subcategoria']}</p>
                <p><b>UC:</b> {it['unidade_conservacao']}</p>
                {f"<p><b>Nome Alternativo:</b> {it['nome_alternativo']}</p>" if it['nome_alternativo'] else ""}
                {f"<p><b>Observações:</b> {it['observacoes']}</p>" if it['observacoes'] else ""}
                {f"<p><b>Data da Coleta:</b> {it['data_coleta']}</p>" if it['data_coleta'] else ""}
                <p><b>Fonte:</b> {it['fonte']}</p>
                <p><b>Coordenadas:</b> {it['latitude']:.6f}, {it['longitude']:.6f}</p>
            ]]>"""
            kml_body += f"""      <Placemark>
        <name>{it['nome']}</name>
        <styleUrl>{s_url}</styleUrl>
        <description>{desc_html}</description>
        <Point>
          <coordinates>{it['longitude']:.6f},{it['latitude']:.6f},0</coordinates>
        </Point>
      </Placemark>\n"""
        kml_body += "    </Folder>\n"
        
    kml_footer = """  </Document>
</kml>"""
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(kml_header + styles + kml_body + kml_footer)
    print(f"Saved: {output_path}")

generate_kml(uc_records, "dados_organizados/pontos_revis_rds_consolidado.kml", "REVIS Tabuleiro do Embaubal e RDS Vitória de Souzel")
if other_records:
    generate_kml(other_records, "dados_organizados/pontos_outras_regioes.kml", "Outros Pontos IDEFLOR-Bio (Pará)")

print("\n--- Pipeline Completed Successfully! ---")
