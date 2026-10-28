import os
import sys
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsCoordinateReferenceSystem,
    QgsRectangle,
    QgsRuleBasedRenderer,
    QgsSingleSymbolRenderer,
    QgsCategorizedSymbolRenderer,
    QgsRendererCategory,
    QgsFillSymbol,
    QgsMarkerSymbol,
    QgsSvgMarkerSymbolLayer,
    QgsSimpleMarkerSymbolLayer,
    QgsSimpleLineSymbolLayer,
    QgsSimpleFillSymbolLayer,
    QgsPalLayerSettings,
    QgsVectorLayerSimpleLabeling,
    QgsTextFormat,
    QgsTextBufferSettings,
    QgsProperty
)
try:
    from PyQt6.QtGui import QColor
except ImportError:
    from PyQt5.QtGui import QColor

# Initialize QGIS Application (headless)
app = QgsApplication([], False)
app.initQgis()

project = QgsProject.instance()
project_file = os.path.abspath("tabuleiro_do_embaubal_e_vitoria_souzel.qgz")

# Read existing or start clean
project.read(project_file)
project.removeAllMapLayers()
project.layerTreeRoot().clear()

# Project Settings
project.setTitle("IDEFLOR-Bio: REVIS Tabuleiro do Embaubal e RDS Vitória de Souzel")
crs_sirgas22s = QgsCoordinateReferenceSystem("EPSG:31982") # SIRGAS 2000 / UTM 22S
project.setCrs(crs_sirgas22s)

root = project.layerTreeRoot()

# Helper to create groups
grp_limites = root.addGroup("01. Limites e Unidades de Conservação")
grp_gestao = root.addGroup("02. Gestão e Infraestrutura")
grp_bio = root.addGroup("03. Biodiversidade e Proteção Ambiental")
grp_comunidades = root.addGroup("04. Comunidades e Uso Tradicional")
grp_hidro = root.addGroup("05. Geografia e Hidrografia")
grp_basemap = root.addGroup("06. Mapas de Fundo (Satélite e Terreno)")

def make_svg_marker(svg_path, color_hex, size_mm, outline_color="#ffffff", outline_width=0.4):
    symbol = QgsMarkerSymbol()
    symbol.deleteSymbolLayer(0) # remove default simple marker
    
    # Bottom circle background
    bg = QgsSimpleMarkerSymbolLayer()
    bg.setShape(QgsSimpleMarkerSymbolLayer.Circle)
    bg.setSize(size_mm + 1.2)
    bg.setColor(QColor(color_hex))
    bg.setStrokeColor(QColor(outline_color))
    bg.setStrokeWidth(outline_width)
    symbol.appendSymbolLayer(bg)
    
    # SVG icon layer
    if os.path.exists(svg_path):
        svg_layer = QgsSvgMarkerSymbolLayer(os.path.relpath(svg_path, "."))
        svg_layer.setSize(size_mm)
        svg_layer.setFillColor(QColor("#ffffff"))
        svg_layer.setStrokeColor(QColor("#333333"))
        svg_layer.setStrokeWidth(0.2)
        symbol.appendSymbolLayer(svg_layer)
    return symbol

def setup_labeling(layer, field_name, min_scale=0, max_scale=150000):
    text_format = QgsTextFormat()
    text_format.setSize(8.5)
    text_format.setColor(QColor("#212529"))
    
    # White buffer (halo)
    buf = QgsTextBufferSettings()
    buf.setEnabled(True)
    buf.setSize(1.0)
    buf.setColor(QColor("#ffffff"))
    text_format.setBuffer(buf)
    
    label_settings = QgsPalLayerSettings()
    label_settings.fieldName = field_name
    label_settings.setFormat(text_format)
    try:
        label_settings.placement = QgsPalLayerSettings.Placement.OrderedPositionsAroundPoint
    except AttributeError:
        pass
    
    simple_labeling = QgsVectorLayerSimpleLabeling(label_settings)
    layer.setLabeling(simple_labeling)
    layer.setLabelsEnabled(True)

# -------------------------------------------------------------
# 1. Unidades de Conservação (Limites)
# -------------------------------------------------------------
ucs_alvo_path = os.path.abspath("camadas/00_ucs_alvo_embaubal_souzel.geojson")
vlayer_ucs_alvo = QgsVectorLayer(ucs_alvo_path, "REVIS Tabuleiro do Embaubal e RDS Vitória de Souzel", "ogr")
if vlayer_ucs_alvo.isValid():
    # Rule based styling for REVIS vs RDS
    root_rule = QgsRuleBasedRenderer.Rule(None)
    
    # Rule 1: REVIS Tabuleiro do Embaubal (Proteção Integral)
    sym_revis = QgsFillSymbol.createSimple({
        "color": "255, 170, 0, 50",       # Amber 20%
        "color_border": "217, 72, 15, 255",# Dark orange
        "width_border": "1.2",
        "style_border": "solid"
    })
    rule_revis = QgsRuleBasedRenderer.Rule(sym_revis)
    rule_revis.setLabel("REVIS Tabuleiro do Embaubal (Proteção Integral)")
    rule_revis.setFilterExpression('"Nome" ILIKE \'%embaubal%\'')
    root_rule.appendChild(rule_revis)
    
    # Rule 2: RDS Vitória de Souzel (Uso Sustentável)
    sym_rds = QgsFillSymbol.createSimple({
        "color": "40, 167, 69, 45",        # Forest Green 18%
        "color_border": "30, 126, 52, 255",# Dark Green
        "width_border": "1.2",
        "style_border": "dash"
    })
    rule_rds = QgsRuleBasedRenderer.Rule(sym_rds)
    rule_rds.setLabel("RDS Vitória de Souzel (Uso Sustentável)")
    rule_rds.setFilterExpression('"Nome" ILIKE \'%souzel%\' OR "Nome" ILIKE \'%vitoria%\'')
    root_rule.appendChild(rule_rds)
    
    renderer = QgsRuleBasedRenderer(root_rule)
    vlayer_ucs_alvo.setRenderer(renderer)
    
    project.addMapLayer(vlayer_ucs_alvo, False)
    grp_limites.addLayer(vlayer_ucs_alvo)

# Demais UCs Estaduais
ucs_todas_path = os.path.abspath("camadas/00_ucs_estaduais_todas.geojson")
vlayer_ucs_todas = QgsVectorLayer(ucs_todas_path, "Demais UCs Estaduais do Pará (Contexto)", "ogr")
if vlayer_ucs_todas.isValid():
    sym_outras = QgsFillSymbol.createSimple({
        "color": "0,0,0,0",
        "color_border": "120, 120, 120, 180",
        "width_border": "0.6",
        "style_border": "dot"
    })
    vlayer_ucs_todas.setRenderer(QgsSingleSymbolRenderer(sym_outras))
    project.addMapLayer(vlayer_ucs_todas, False)
    node_outras = grp_limites.addLayer(vlayer_ucs_todas)
    node_outras.setItemVisibilityChecked(False) # Off by default

# -------------------------------------------------------------
# 2. Gestão e Infraestrutura
# -------------------------------------------------------------
# 06 Infraestrutura e Equipamentos
infra_path = os.path.abspath("camadas/06_infraestrutura_e_equipamentos.geojson")
vl_infra = QgsVectorLayer(infra_path, "Infraestrutura e Equipamentos Públicos", "ogr")
if vl_infra.isValid():
    sym = make_svg_marker("simbologia/maki/ranger-station.svg", "#d90429", 5.0)
    vl_infra.setRenderer(QgsSingleSymbolRenderer(sym))
    setup_labeling(vl_infra, "nome")
    project.addMapLayer(vl_infra, False)
    grp_gestao.addLayer(vl_infra)

# 10 Trajetos e Acessos
trajetos_path = os.path.abspath("camadas/10_trajetos_e_acessos.geojson")
vl_trajetos = QgsVectorLayer(trajetos_path, "Trajetos e Acessos", "ogr")
if vl_trajetos.isValid():
    sym = QgsMarkerSymbol.createSimple({
        "name": "triangle",
        "color": "114, 9, 183, 200",
        "color_border": "#ffffff",
        "size": "3.5",
        "width_border": "0.4"
    })
    vl_trajetos.setRenderer(QgsSingleSymbolRenderer(sym))
    project.addMapLayer(vl_trajetos, False)
    grp_gestao.addLayer(vl_trajetos)

# 09 Ocorrências e Impactos
fogo_path = os.path.abspath("camadas/09_ocorrencias_e_impactos.geojson")
vl_fogo = QgsVectorLayer(fogo_path, "Ocorrências e Impactos (Fogo/Búfalos)", "ogr")
if vl_fogo.isValid():
    sym = make_svg_marker("simbologia/ian-symbols/Ecosystems/Elements/fire.svg", "#ff4800", 5.2)
    vl_fogo.setRenderer(QgsSingleSymbolRenderer(sym))
    setup_labeling(vl_fogo, "nome")
    project.addMapLayer(vl_fogo, False)
    grp_gestao.addLayer(vl_fogo)

# -------------------------------------------------------------
# 3. Biodiversidade e Proteção Ambiental
# -------------------------------------------------------------
# 03 Áreas de Desova (Quelônios e Peixes)
desova_path = os.path.abspath("camadas/03_areas_de_desova.geojson")
vl_desova = QgsVectorLayer(desova_path, "Áreas de Desova (Quelônios e Peixes)", "ogr")
if vl_desova.isValid():
    sym = make_svg_marker("simbologia/ian-symbols/Fauna/Reptiles/caretta-caretta-loggerhead-turtle.svg", "#007f5f", 5.5, outline_color="#ffff3f", outline_width=0.8)
    vl_desova.setRenderer(QgsSingleSymbolRenderer(sym))
    setup_labeling(vl_desova, "nome")
    project.addMapLayer(vl_desova, False)
    grp_bio.addLayer(vl_desova)

# 08 Vegetação e Flora (Árvores Matrizes)
flora_path = os.path.abspath("camadas/08_vegetacao_e_flora.geojson")
vl_flora = QgsVectorLayer(flora_path, "Vegetação e Flora (Árvores Matrizes)", "ogr")
if vl_flora.isValid():
    sym = make_svg_marker("simbologia/maki/park.svg", "#2b9348", 4.2)
    vl_flora.setRenderer(QgsSingleSymbolRenderer(sym))
    project.addMapLayer(vl_flora, False)
    grp_bio.addLayer(vl_flora)

# -------------------------------------------------------------
# 4. Comunidades e Uso Tradicional
# -------------------------------------------------------------
# 01 Moradores e Comunidades
moradores_path = os.path.abspath("camadas/01_moradores_e_comunidades.geojson")
vl_moradores = QgsVectorLayer(moradores_path, "Moradores e Comunidades Ribeirinhas", "ogr")
if vl_moradores.isValid():
    sym = make_svg_marker("simbologia/maki/home.svg", "#f77f00", 4.0)
    vl_moradores.setRenderer(QgsSingleSymbolRenderer(sym))
    setup_labeling(vl_moradores, "nome")
    project.addMapLayer(vl_moradores, False)
    grp_comunidades.addLayer(vl_moradores)

# 02 Apoio de Pesca e Ranchos
pesca_path = os.path.abspath("camadas/02_apoio_de_pesca_e_ranchos.geojson")
vl_pesca = QgsVectorLayer(pesca_path, "Apoio de Pesca e Ranchos", "ogr")
if vl_pesca.isValid():
    sym = make_svg_marker("simbologia/maki/fishing.svg", "#0096c7", 4.0)
    vl_pesca.setRenderer(QgsSingleSymbolRenderer(sym))
    project.addMapLayer(vl_pesca, False)
    grp_comunidades.addLayer(vl_pesca)

# -------------------------------------------------------------
# 5. Geografia e Hidrografia
# -------------------------------------------------------------
# 05 Ilhas e Praias
ilhas_path = os.path.abspath("camadas/05_ilhas_e_praias.geojson")
vl_ilhas = QgsVectorLayer(ilhas_path, "Ilhas e Praias (Bancos de Areia)", "ogr")
if vl_ilhas.isValid():
    sym = make_svg_marker("simbologia/maki/beach.svg", "#d4a373", 4.2)
    vl_ilhas.setRenderer(QgsSingleSymbolRenderer(sym))
    setup_labeling(vl_ilhas, "nome")
    project.addMapLayer(vl_ilhas, False)
    grp_hidro.addLayer(vl_ilhas)

# 04 Hidrografia
hidro_path = os.path.abspath("camadas/04_hidrografia.geojson")
vl_hidro = QgsVectorLayer(hidro_path, "Hidrografia (Rios, Furos e Igarapés)", "ogr")
if vl_hidro.isValid():
    sym = make_svg_marker("simbologia/maki/water.svg", "#0077b6", 3.8)
    vl_hidro.setRenderer(QgsSingleSymbolRenderer(sym))
    setup_labeling(vl_hidro, "nome")
    project.addMapLayer(vl_hidro, False)
    grp_hidro.addLayer(vl_hidro)

# 07 Marcos e Pontos de Referência
marcos_path = os.path.abspath("camadas/07_marcos_e_pontos_referencia.geojson")
vl_marcos = QgsVectorLayer(marcos_path, "Marcos e Pontos de Referência", "ogr")
if vl_marcos.isValid():
    sym = make_svg_marker("simbologia/maki/marker.svg", "#495057", 3.8)
    vl_marcos.setRenderer(QgsSingleSymbolRenderer(sym))
    project.addMapLayer(vl_marcos, False)
    grp_hidro.addLayer(vl_marcos)

# -------------------------------------------------------------
# 6. Basemaps (XYZ Tiles de Satélite)
# -------------------------------------------------------------
google_sat_url = "type=xyz&url=https://mt1.google.com/vt/lyrs%3Ds%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D"
rl_google_sat = QgsRasterLayer(google_sat_url, "Google Satellite", "wms")
if rl_google_sat.isValid():
    project.addMapLayer(rl_google_sat, False)
    grp_basemap.addLayer(rl_google_sat)

esri_sat_url = "type=xyz&url=https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D"
rl_esri_sat = QgsRasterLayer(esri_sat_url, "ESRI World Imagery", "wms")
if rl_esri_sat.isValid():
    project.addMapLayer(rl_esri_sat, False)
    node_esri = grp_basemap.addLayer(rl_esri_sat)
    node_esri.setItemVisibilityChecked(False)

osm_url = "type=xyz&url=https://tile.openstreetmap.org/%7Bz%7D/%7By%7D/%7Bx%7D.png"
rl_osm = QgsRasterLayer(osm_url, "OpenStreetMap Standard", "wms")
if rl_osm.isValid():
    project.addMapLayer(rl_osm, False)
    node_osm = grp_basemap.addLayer(rl_osm)
    node_osm.setItemVisibilityChecked(False)

# Set relative paths mode
try:
    project.setFilePathStorage(QgsProject.FilePathStorage.Relative)
except Exception:
    pass

# Save project
ok = project.write(project_file)
print(f"Project saved successfully: {ok} -> {project_file}")

app.exitQgis()
