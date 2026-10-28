# -*- coding: utf-8 -*-
"""
Calcula as transições de uso da terra entre 1985 e 2024 para o diagrama de Sankey.
"""
from qgis.core import QgsApplication, QgsRasterLayer, QgsVectorLayer, QgsPointXY
from collections import defaultdict
import json

QgsApplication.setPrefixPath('C:/Program Files/QGIS 4.2.3/apps/qgis', True)
qgs = QgsApplication([], False)
qgs.initQgis()

rast = QgsRasterLayer('camadas/raster/mapbiomas_c11_temporal_1985_2024.tif', 'temp')
vec = QgsVectorLayer('camadas/00_ucs_alvo_embaubal_souzel.geojson', 'vec', 'ogr')

dp = rast.dataProvider()
ext = rast.extent()
w, h = rast.width(), rast.height()
x_res = (ext.xMaximum() - ext.xMinimum()) / w
y_res = (ext.yMaximum() - ext.yMinimum()) / h

b1 = dp.block(1, ext, w, h) # 1985
b5 = dp.block(5, ext, w, h) # 2024

geoms = [f.geometry() for f in vec.getFeatures()]
transitions = defaultdict(int)

for geom in geoms:
    bbox = geom.boundingBox()
    col_min = max(0, int((bbox.xMinimum() - ext.xMinimum()) / x_res))
    col_max = min(w - 1, int((bbox.xMaximum() - ext.xMinimum()) / x_res))
    row_min = max(0, int((ext.yMaximum() - bbox.yMaximum()) / y_res))
    row_max = min(h - 1, int((ext.yMaximum() - bbox.yMinimum()) / y_res))

    for r in range(row_min, row_max + 1):
        y_c = ext.yMaximum() - (r + 0.5) * y_res
        for c in range(col_min, col_max + 1):
            x_c = ext.xMinimum() + (c + 0.5) * x_res
            if geom.contains(QgsPointXY(x_c, y_c)):
                v85 = int(b1.value(r, c))
                v24 = int(b5.value(r, c))
                if v85 > 0 and v24 > 0:
                    transitions[(v85, v24)] += 1

tot_pix = sum(transitions.values())
ha_per_pix = 27023.12 / tot_pix

trans_list = []
print(f"Total pixels analisados: {tot_pix:,} ({tot_pix * ha_per_pix:,.2f} ha)")
print("\nPrincipais Transições (1985 -> 2024):")
for (v85, v24), count in sorted(transitions.items(), key=lambda x: -x[1]):
    ha = count * ha_per_pix
    pct = (count / tot_pix) * 100.0
    trans_list.append({'from': v85, 'to': v24, 'ha': ha, 'pct': pct, 'pixels': count})
    if ha >= 10.0:
        print(f"  {v85:2d} -> {v24:2d} : {ha:8.1f} ha ({pct:5.2f}%)")

with open('camadas/tabelas/transicoes_mapbiomas_1985_2024.json', 'w', encoding='utf-8') as f:
    json.dump(trans_list, f, ensure_ascii=False, indent=2)

print("\nArquivo salvo: camadas/tabelas/transicoes_mapbiomas_1985_2024.json")
qgs.exitQgis()
