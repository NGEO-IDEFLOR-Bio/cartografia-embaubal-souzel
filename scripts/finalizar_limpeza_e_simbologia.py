# -*- coding: utf-8 -*-
"""
Finalização da Limpeza Cartográfica e Atualização da Simbologia QGIS
1. Consolida pontos limpos em pontos_revis_rds_consolidado.geojson e .gpkg
2. Aumenta tamanho da simbologia de Quelônios (de 5.5mm para 8.5mm / 10.0mm)
3. Insere marcador institucional nobre para a BASE DO IDEFLOR-BIO
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import geopandas as gpd
import pandas as pd

DIR_CAMADAS = "camadas"
QGZ_PATH = "tabuleiro_do_embaubal_e_vitoria_souzel.qgz"

# -------------------------------------------------------------
# 1. Reconsolidação da camada geral de pontos
# -------------------------------------------------------------
print("--- [1/2] Consolidando pontos limpos ---")
camadas_pontos = [
    '01_moradores_e_comunidades.geojson',
    '02_apoio_de_pesca_e_ranchos.geojson',
    '03_areas_de_desova.geojson',
    '04_hidrografia.geojson',
    '05_ilhas_e_praias.geojson',
    '06_infraestrutura_e_equipamentos.geojson',
    '07_marcos_e_pontos_referencia.geojson',
    '08_vegetacao_e_flora.geojson',
    '09_ocorrencias_e_impactos.geojson'
]

gdfs = []
for c in camadas_pontos:
    p = os.path.join(DIR_CAMADAS, c)
    if os.path.exists(p):
        g = gpd.read_file(p)
        if len(g) > 0:
            gdfs.append(g.to_crs(epsg=4674))
            print(f"  + {c}: {len(g)} pontos")

gdf_cons = pd.concat(gdfs, ignore_index=True)
gdf_cons = gpd.GeoDataFrame(gdf_cons, geometry='geometry', crs="EPSG:4674")

gdf_cons.to_file(f"{DIR_CAMADAS}/pontos_revis_rds_consolidado.geojson", driver="GeoJSON", encoding="utf-8")
gdf_cons.to_file(f"{DIR_CAMADAS}/pontos_revis_rds_consolidado.gpkg", layer="pontos_campo", driver="GPKG")
print(f"[OK] Total geral consolidado: {len(gdf_cons)} pontos únicos e limpos.")

# Garante que 10_trajetos_e_acessos.geojson seja um GeoJSON vazio válido
empty_trajetos = gpd.GeoDataFrame({'id': [], 'nome': [], 'categoria': [], 'subcategoria': []}, geometry=[], crs="EPSG:4674")
empty_trajetos.to_file(f"{DIR_CAMADAS}/10_trajetos_e_acessos.geojson", driver="GeoJSON", encoding="utf-8")

# -------------------------------------------------------------
# 2. Atualização da Simbologia no QGIS (.qgz)
# -------------------------------------------------------------
print("\n--- [2/2] Atualizando simbologia no QGZ ---")

with zipfile.ZipFile(QGZ_PATH, 'r') as z:
    qgs_bytes = z.read("tabuleiro_do_embaubal_e_vitoria_souzel.qgs")
    outras_partes = {n: z.read(n) for n in z.namelist() if n != "tabuleiro_do_embaubal_e_vitoria_souzel.qgs"}

root = ET.fromstring(qgs_bytes)

# A. Aumenta tamanho de Quelônios
for ml in root.findall(".//maplayer"):
    lname = str(ml.find('layername').text if ml.find('layername') is not None else '')
    if any(k in lname.lower() for k in ['desova', 'quelônios', 'quelonios']):
        print(f"  • Aumentando ícones de Quelônios na camada: {lname}")
        renderer = ml.find('renderer-v2')
        if renderer is not None:
            # SimpleMarker: fundo circular de 6.7mm -> 10.5mm
            for opt in renderer.findall(".//layer[@class='SimpleMarker']//Option"):
                if opt.attrib.get('name') == 'size':
                    opt.attrib['value'] = "10.5"
                elif opt.attrib.get('name') == 'outline_width':
                    opt.attrib['value'] = "1.0"
            # SvgMarker: tartaruga de 5.5mm -> 8.8mm
            for opt in renderer.findall(".//layer[@class='SvgMarker']//Option"):
                if opt.attrib.get('name') == 'size':
                    opt.attrib['value'] = "8.8"

# B. Marcador diferenciado e imponente para a BASE DO IDEFLOR-BIO
for ml in root.findall(".//maplayer"):
    lid = str(ml.find('id').text if ml.find('id') is not None else '')
    lname = str(ml.find('layername').text if ml.find('layername') is not None else '')
    if 'base_ideflor' in lid.lower() or 'base do ideflor' in lname.lower():
        print(f"  • Configurando marcador institucional nobre para: {lname}")
        renderer = ml.find('renderer-v2')
        if renderer is not None:
            symbols = renderer.find('symbols')
            if symbols is not None and len(symbols) > 0:
                sym = symbols[0]
                for old_l in list(sym.findall('layer')):
                    sym.remove(old_l)

                # Camada 1: Círculo exterior Verde Floresta IDEFLOR com borda Dourada
                l1 = ET.SubElement(sym, 'layer', {
                    'class': 'SimpleMarker', 'enabled': '1', 'locked': '0', 'pass': '0',
                    'id': '{base_ideflor_bg}'
                })
                opts1 = {
                    'angle': '0',
                    'color': '14,77,42,255',            # Verde Floresta Oficial (#0E4D2A)
                    'name': 'circle',
                    'size': '11.5',                     # Destaque de 11.5 mm
                    'size_unit': 'MM',
                    'outline_color': '241,196,15,255',  # Borda Dourada (#F1C40F)
                    'outline_style': 'solid',
                    'outline_width': '1.2',
                    'outline_width_unit': 'MM'
                }
                for k, v in opts1.items():
                    ET.SubElement(l1, 'Option', {'name': k, 'type': 'QString', 'value': v})

                # Camada 2: Anel interno branco
                l2 = ET.SubElement(sym, 'layer', {
                    'class': 'SimpleMarker', 'enabled': '1', 'locked': '0', 'pass': '0',
                    'id': '{base_ideflor_ring}'
                })
                opts2 = {
                    'angle': '0',
                    'color': '0,0,0,0',
                    'name': 'circle',
                    'size': '9.2',
                    'size_unit': 'MM',
                    'outline_color': '255,255,255,230',
                    'outline_style': 'solid',
                    'outline_width': '0.5',
                    'outline_width_unit': 'MM'
                }
                for k, v in opts2.items():
                    ET.SubElement(l2, 'Option', {'name': k, 'type': 'QString', 'value': v})

                # Camada 3: Ícone SVG Ranger Station em branco
                l3 = ET.SubElement(sym, 'layer', {
                    'class': 'SvgMarker', 'enabled': '1', 'locked': '0', 'pass': '0',
                    'id': '{base_ideflor_icon}'
                })
                opts3 = {
                    'name': './simbologia/maki/ranger-station.svg',
                    'color': '255,255,255,255',
                    'outline_color': '14,77,42,255',
                    'outline_width': '0.1',
                    'size': '7.0',
                    'size_unit': 'MM'
                }
                for k, v in opts3.items():
                    ET.SubElement(l3, 'Option', {'name': k, 'type': 'QString', 'value': v})

# Salva QGS e recompacta QGZ
qgs_atualizado = ET.tostring(root, encoding="utf-8", xml_declaration=True)

with zipfile.ZipFile(QGZ_PATH, 'w', compression=zipfile.ZIP_DEFLATED) as z_out:
    z_out.writestr("tabuleiro_do_embaubal_e_vitoria_souzel.qgs", qgs_atualizado)
    for n, data in outras_partes.items():
        z_out.writestr(n, data)

print(f"\n[SUCESSO COMPLETO] Limpeza concluída e projeto QGIS atualizado com sucesso!")
