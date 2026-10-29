# -*- coding: utf-8 -*-
"""
Injeção das Camadas do Tema Fogo diretamente no arquivo QGIS (.qgz)
Projeto: tabuleiro_do_embaubal_e_vitoria_souzel.qgz

Atualiza:
1. <projectlayers>: Adiciona as 5 camadas com renderizadores oficiais singleSymbol.
2. <layer-tree-group>: Insere as camadas dentro do grupo '08. QUEIMADAS'.
3. <layerorder>: Garante a ordenação correta das novas camadas no projeto.
"""

import zipfile
import shutil
import os
import xml.etree.ElementTree as ET
import copy

QGZ_PATH = "tabuleiro_do_embaubal_e_vitoria_souzel.qgz"
BAK_PATH = "tabuleiro_do_embaubal_e_vitoria_souzel.qgz.bak"

# 1. Cria backup de segurança
if not os.path.exists(BAK_PATH):
    shutil.copy2(QGZ_PATH, BAK_PATH)
    print(f"[OK] Backup criado em: {BAK_PATH}")

CAMADAS = [
    {
        "id": "Fogo_2015_2024_mapbiomas_c31",
        "name": "Cicatrizes de Fogo (2015 – 2024)",
        "source": "./camadas/mapbiomas-fogo/agrupado/fogo_2015_2024.shp",
        "fill_color": "144,12,63,190",      # Carmim Bordeaux
        "stroke_color": "88,24,69,255",
        "stroke_width": "0.3",
        "stroke_style": "solid",
        "fill_style": "solid",
        "checked": "Qt::Checked"
    },
    {
        "id": "Fogo_2005_2014_mapbiomas_c31",
        "name": "Cicatrizes de Fogo (2005 – 2014)",
        "source": "./camadas/mapbiomas-fogo/agrupado/fogo_2005_2014.shp",
        "fill_color": "231,76,60,180",      # Vermelho Escarlate
        "stroke_color": "146,43,33,255",
        "stroke_width": "0.3",
        "stroke_style": "solid",
        "fill_style": "solid",
        "checked": "Qt::Unchecked"
    },
    {
        "id": "Fogo_1995_2004_mapbiomas_c31",
        "name": "Cicatrizes de Fogo (1995 – 2004)",
        "source": "./camadas/mapbiomas-fogo/agrupado/fogo_1995_2004.shp",
        "fill_color": "230,126,34,180",     # Laranja Queimado
        "stroke_color": "160,64,0,255",
        "stroke_width": "0.3",
        "stroke_style": "solid",
        "fill_style": "solid",
        "checked": "Qt::Unchecked"
    },
    {
        "id": "Fogo_1985_1994_mapbiomas_c31",
        "name": "Cicatrizes de Fogo (1985 – 1994)",
        "source": "./camadas/mapbiomas-fogo/agrupado/fogo_1985_1994.shp",
        "fill_color": "243,156,18,180",     # Âmbar Dourado
        "stroke_color": "185,119,14,255",
        "stroke_width": "0.3",
        "stroke_style": "solid",
        "fill_style": "solid",
        "checked": "Qt::Unchecked"
    },
    {
        "id": "Buffer_Externo_2km_UCs_fogo",
        "name": "Zona de Amortecimento (Buffer 2 km UCs)",
        "source": "./camadas/mapbiomas-fogo/Buffer_Externo_2km_UCs.shp",
        "fill_color": "0,0,0,0",            # Transparente
        "stroke_color": "192,57,43,220",    # Vermelho borda
        "stroke_width": "0.6",
        "stroke_style": "dash",
        "fill_style": "no",
        "checked": "Qt::Checked"
    }
]

# 2. Abre o QGZ e lê o QGS
with zipfile.ZipFile(QGZ_PATH, 'r') as z:
    qgs_bytes = z.read("tabuleiro_do_embaubal_e_vitoria_souzel.qgs")
    outras_partes = {n: z.read(n) for n in z.namelist() if n != "tabuleiro_do_embaubal_e_vitoria_souzel.qgs"}

root = ET.fromstring(qgs_bytes)

# Localiza uma camada poligonal existente como molde de atributos
template_layer = None
for ml in root.findall(".//maplayer"):
    if ml.attrib.get("type") == "vector" and ml.attrib.get("geometry") == "Polygon":
        template_layer = ml
        break

if template_layer is None:
    raise ValueError("Não foi encontrada camada vetorial poligonal de referência.")

projectlayers = root.find("projectlayers")
layerorder = root.find("layerorder")

# Localiza o grupo 08. QUEIMADAS na árvore de camadas
grupo_fogo = None
for grp in root.findall(".//layer-tree-group"):
    if grp.attrib.get("name") == "08. QUEIMADAS":
        grupo_fogo = grp
        break

if grupo_fogo is None:
    # Se não encontrar, busca o root layer-tree-group
    lt_root = root.find("layer-tree-group")
    grupo_fogo = ET.SubElement(lt_root, "layer-tree-group", {
        "checked": "Qt::Checked",
        "expanded": "1",
        "groupLayer": "",
        "name": "08. QUEIMADAS",
        "wms-group-request-mode": "Normal"
    })

# Remove camadas antigas se já tiverem sido injetadas anteriormente
ids_fogo = [c["id"] for c in CAMADAS]

for ml in list(projectlayers.findall("maplayer")):
    if ml.find("id") is not None and ml.find("id").text in ids_fogo:
        projectlayers.remove(ml)

for item in list(grupo_fogo.findall("layer-tree-layer")):
    if item.attrib.get("id") in ids_fogo:
        grupo_fogo.remove(item)

if layerorder is not None:
    for item in list(layerorder.findall("item")):
        if item.text in ids_fogo:
            layerorder.remove(item)

# Injeta cada nova camada
for cfg in CAMADAS:
    new_ml = copy.deepcopy(template_layer)
    
    # Atualiza identificadores básicos
    new_ml.find("id").text = cfg["id"]
    new_ml.find("layername").text = cfg["name"]
    new_ml.find("datasource").text = cfg["source"]
    if new_ml.find("provider") is not None:
        new_ml.find("provider").text = "ogr"

    # Atualiza o renderizador de símbolo
    renderer = new_ml.find("renderer-v2")
    if renderer is not None:
        renderer.attrib["type"] = "singleSymbol"
        symbols = renderer.find("symbols")
        if symbols is not None and len(symbols) > 0:
            sym = symbols[0]
            layer_sym = sym.find("layer")
            if layer_sym is not None:
                layer_sym.attrib["class"] = "SimpleFill"
                # Remove opções existentes de cor/stroke e define as novas
                for opt in list(layer_sym.findall("Option")):
                    name = opt.attrib.get("name")
                    if name in ["color", "outline_color", "outline_width", "outline_style", "style"]:
                        layer_sym.remove(opt)
                
                ET.SubElement(layer_sym, "Option", {"name": "color", "type": "QString", "value": cfg["fill_color"]})
                ET.SubElement(layer_sym, "Option", {"name": "outline_color", "type": "QString", "value": cfg["stroke_color"]})
                ET.SubElement(layer_sym, "Option", {"name": "outline_width", "type": "QString", "value": cfg["stroke_width"]})
                ET.SubElement(layer_sym, "Option", {"name": "outline_width_unit", "type": "QString", "value": "MM"})
                ET.SubElement(layer_sym, "Option", {"name": "outline_style", "type": "QString", "value": cfg["stroke_style"]})
                ET.SubElement(layer_sym, "Option", {"name": "style", "type": "QString", "value": cfg["fill_style"]})

    # Adiciona a camada em projectlayers
    projectlayers.append(new_ml)

    # Adiciona na árvore de camadas dentro de 08. QUEIMADAS
    tree_layer = ET.SubElement(grupo_fogo, "layer-tree-layer", {
        "checked": cfg["checked"],
        "expanded": "1",
        "id": cfg["id"],
        "legend_exp": "",
        "legend_split_behavior": "0",
        "name": cfg["name"],
        "patch_size": "-1,-1",
        "providerKey": "ogr",
        "source": cfg["source"]
    })

    # Adiciona em layerorder
    if layerorder is not None:
        item_lo = ET.SubElement(layerorder, "item")
        item_lo.text = cfg["id"]

    print(f"[+] Injetada camada no QGZ: {cfg['name']}")

# Salva QGS atualizado e recompacta QGZ
qgs_atualizado = ET.tostring(root, encoding="utf-8", xml_declaration=True)

with zipfile.ZipFile(QGZ_PATH, 'w', compression=zipfile.ZIP_DEFLATED) as z_out:
    z_out.writestr("tabuleiro_do_embaubal_e_vitoria_souzel.qgs", qgs_atualizado)
    for n, data in outras_partes.items():
        z_out.writestr(n, data)

print(f"\n[SUCESSO] Projeto QGIS ({QGZ_PATH}) atualizado com as camadas de Queimadas no grupo '08. QUEIMADAS'!")
