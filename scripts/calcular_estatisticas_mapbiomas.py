# -*- coding: utf-8 -*-
"""
Script: Quantificação de Classes MapBiomas Coleção 11 por Unidade de Conservação
Calcula a área em hectares e a porcentagem de cada classe de uso/cobertura
para cada ano da série temporal (1985, 1995, 2005, 2015, 2024) para o:
1. REVIS Tabuleiro do Embaubal
2. RDS Vitória de Souzel

Pode ser executado no Console Python do QGIS ou via terminal.
"""

import os
import json
import csv
from collections import defaultdict

from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsGeometry,
    QgsPointXY,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem
)

# Inicia QgsApplication se rodando fora do QGIS GUI
app_iniciada = False
if not QgsProject.instance().fileName() and not globals().get('iface'):
    QgsApplication.setPrefixPath("C:/Program Files/QGIS 4.2.3/apps/qgis", True)
    qgs_app = QgsApplication([], False)
    qgs_app.initQgis()
    app_iniciada = True

# TABELA OFICIAL MAPBIOMAS COLEÇÃO 11
CLASSES_MAPBIOMAS_C11 = {
    1:  {'hex': '#1f8d49', 'nome': 'Floresta'},
    3:  {'hex': '#1f8d49', 'nome': 'Formação Florestal'},
    6:  {'hex': '#007785', 'nome': 'Floresta Alagável'},
    4:  {'hex': '#7dc975', 'nome': 'Formação Savânica'},
    7:  {'hex': '#228c70', 'nome': 'Savana Alagada'},
    5:  {'hex': '#04381d', 'nome': 'Mangue'},
    49: {'hex': '#02d659', 'nome': 'Restinga Arbórea'},
    10: {'hex': '#d6bc74', 'nome': 'Veg. Herbácea e Arbustiva'},
    12: {'hex': '#d6bc74', 'nome': 'Formação Campestre'},
    77: {'hex': '#86b074', 'nome': 'Formação Herbáceo Arbustiva'},
    11: {'hex': '#519799', 'nome': 'Campo Alagado e Área Pantanosa'},
    84: {'hex': '#81dbbf', 'nome': 'Marisma'},
    50: {'hex': '#ffaa5f', 'nome': 'Restinga Herbácea'},
    32: {'hex': '#fc8114', 'nome': 'Apicum'},
    29: {'hex': '#ad5100', 'nome': 'Afloramento Rochoso'},
    14: {'hex': '#ffefc3', 'nome': 'Agropecuária'},
    15: {'hex': '#edde8e', 'nome': 'Pastagem'},
    18: {'hex': '#E974ED', 'nome': 'Agricultura'},
    19: {'hex': '#C27BA0', 'nome': 'Lavoura Temporária'},
    39: {'hex': '#f5b3c8', 'nome': 'Soja'},
    20: {'hex': '#db7093', 'nome': 'Cana'},
    40: {'hex': '#c71585', 'nome': 'Arroz'},
    62: {'hex': '#ff69b4', 'nome': 'Algodão'},
    41: {'hex': '#f54ca9', 'nome': 'Outras Lavouras Temporárias'},
    36: {'hex': '#d082de', 'nome': 'Lavoura Perene'},
    46: {'hex': '#d68fe2', 'nome': 'Café'},
    47: {'hex': '#9932cc', 'nome': 'Citrus'},
    35: {'hex': '#9065d0', 'nome': 'Dendê'},
    48: {'hex': '#e6ccff', 'nome': 'Outras Lavouras Perenes'},
    9:  {'hex': '#7a5900', 'nome': 'Silvicultura'},
    21: {'hex': '#ffefc3', 'nome': 'Mosaico de Usos'},
    22: {'hex': '#d4271e', 'nome': 'Área não Vegetada'},
    23: {'hex': '#ffa07a', 'nome': 'Praia, Duna e Areal'},
    24: {'hex': '#d4271e', 'nome': 'Área Urbanizada'},
    30: {'hex': '#9c0027', 'nome': 'Mineração'},
    75: {'hex': '#757272', 'nome': 'Usina Fotovoltaica'},
    91: {'hex': '#403d3e', 'nome': 'Parque Eólico'},
    25: {'hex': '#db4d4f', 'nome': 'Outras Áreas não Vegetadas'},
    26: {'hex': '#2532e4', 'nome': 'Corpo D\'Água'},
    33: {'hex': '#2532e4', 'nome': 'Rio, Lago e Oceano'},
    31: {'hex': '#091077', 'nome': 'Aquicultura'},
    27: {'hex': '#ffffff', 'nome': 'Não Observado'}
}

ANOS_MAPA = {
    1: 1985,
    2: 1995,
    3: 2005,
    4: 2015,
    5: 2024
}

def calcular():
    # 1. Localizar Vetor das UCs e Raster Temporal
    vec_path = "camadas/00_ucs_alvo_embaubal_souzel.geojson"
    rast_path = "camadas/raster/mapbiomas_c11_temporal_1985_2024.tif"
    
    # Se estiver rodando dentro do QGIS, tenta usar camadas do projeto se disponíveis
    vec_layer = None
    rast_layer = None
    
    for l in QgsProject.instance().mapLayers().values():
        if '00_ucs_alvo' in l.source() or 'revis tabuleiro' in l.name().lower():
            vec_layer = l
        if 'temporal' in l.source() or 'temporal' in l.name().lower():
            rast_layer = l

    if not vec_layer or not vec_layer.isValid():
        vec_layer = QgsVectorLayer(vec_path, "ucs_alvo", "ogr")
    if not rast_layer or not rast_layer.isValid():
        rast_layer = QgsRasterLayer(rast_path, "mapbiomas_temporal")

    if not vec_layer.isValid() or not rast_layer.isValid():
        print(f"[ERRO] Camadas não puderam ser carregadas.\nVetor: {vec_path}\nRaster: {rast_path}")
        return

    print("================================================================================")
    print("CALCULANDO ESTATÍSTICAS MAPBIOMAS COLEÇÃO 11 PARA AS UCs")
    print(f"Vetor: {vec_layer.name()} ({vec_layer.featureCount()} feições)")
    print(f"Raster: {rast_layer.name()} ({rast_layer.bandCount()} bandas)")
    print("================================================================================")

    provider = rast_layer.dataProvider()
    extent = rast_layer.extent()
    width = rast_layer.width()
    height = rast_layer.height()
    x_res = (extent.xMaximum() - extent.xMinimum()) / width
    y_res = (extent.yMaximum() - extent.yMinimum()) / height
    
    # Transformação de coordenadas se necessário
    crs_rast = rast_layer.crs()
    crs_vec = vec_layer.crs()
    transform = None
    if crs_rast != crs_vec:
        transform = QgsCoordinateTransform(crs_vec, crs_rast, QgsProject.instance())

    # Área exata do pixel em hectares (30m x 30m = 900 m² = 0.09 ha)
    # No CRS EPSG:4674 a latitude média é -2.77 graus.
    # 1 grau lon ~ 111.19 * cos(-2.77°) ~ 111.06 km -> 0.0002695 deg ~ 29.93m
    # 1 grau lat ~ 110.57 km -> 0.0002695 deg ~ 29.80m
    # Área por pixel ~ 29.93 * 29.80 = 891.9 m² ~ 0.08919 ha (aprox 0.09 ha)
    # Vamos usar a área proporcional da geometria para exatidão perfeita.
    
    # Pré-carregar todas as bandas em blocos
    blocos = {}
    for b in range(1, rast_layer.bandCount() + 1):
        blocos[b] = provider.block(b, extent, width, height)

    resultados = []

    for feat in vec_layer.getFeatures():
        nome_uc = feat["Nome"]
        cat_uc = feat["Categoria"]
        geom = feat.geometry()
        if transform:
            geom.transform(transform)

        bbox = geom.boundingBox()
        # Coordenadas em pixels da bounding box
        col_min = max(0, int((bbox.xMinimum() - extent.xMinimum()) / x_res))
        col_max = min(width - 1, int((bbox.xMaximum() - extent.xMinimum()) / x_res))
        row_min = max(0, int((extent.yMaximum() - bbox.yMaximum()) / y_res))
        row_max = min(height - 1, int((extent.yMaximum() - bbox.yMinimum()) / y_res))

        print(f"\n-> Processando: {nome_uc} ({cat_uc})...")

        # Mapeia quais pixels estão dentro do polígono
        pixels_internos = []
        for r in range(row_min, row_max + 1):
            y_coord = extent.yMaximum() - (r + 0.5) * y_res
            for c in range(col_min, col_max + 1):
                x_coord = extent.xMinimum() + (c + 0.5) * x_res
                pt = QgsPointXY(x_coord, y_coord)
                if geom.contains(pt):
                    pixels_internos.append((r, c))

        total_pixels = len(pixels_internos)
        print(f"   Pixels contidos no polígono: {total_pixels:,}")

        # Contabilizar classes para cada ano
        dados_uc = {
            "unidade": nome_uc,
            "categoria": cat_uc,
            "total_pixels": total_pixels,
            "anos": {}
        }

        # Área de cada pixel estimada em hectares com base na área declarada/calculada da UC
        # Isso garante que a soma de todas as classes bata exatamente com o total da UC!
        area_calculada_ha = feat["Área Calculada (ha)"]
        if area_calculada_ha and float(area_calculada_ha) > 0:
            ha_por_pixel = float(area_calculada_ha) / total_pixels
        else:
            ha_por_pixel = 0.0892  # Fallback 30m

        area_total_ha = total_pixels * ha_por_pixel

        for b, ano in ANOS_MAPA.items():
            if b > rast_layer.bandCount():
                continue
            bloco = blocos[b]
            contagem = defaultdict(int)
            for r, c in pixels_internos:
                val = int(bloco.value(r, c))
                if val > 0:
                    contagem[val] += 1

            classes_ano = []
            for cid, count in sorted(contagem.items(), key=lambda x: -x[1]):
                classe_info = CLASSES_MAPBIOMAS_C11.get(cid, {'nome': f'Classe {cid}', 'hex': '#888888'})
                ha = count * ha_por_pixel
                pct = (count / total_pixels) * 100.0 if total_pixels > 0 else 0
                classes_ano.append({
                    "id": cid,
                    "nome": classe_info['nome'],
                    "hex": classe_info['hex'],
                    "pixels": count,
                    "area_ha": round(ha, 2),
                    "percentual": round(pct, 2)
                })

            dados_uc["anos"][str(ano)] = {
                "ano": ano,
                "area_total_ha": round(area_total_ha, 2),
                "classes": classes_ano
            }

        resultados.append(dados_uc)

    # 4. Salvar resultados em JSON e CSV
    os.makedirs("camadas/tabelas", exist_ok=True)
    json_path = "camadas/tabelas/estatisticas_mapbiomas_c11_ucs.json"
    csv_path = "camadas/tabelas/estatisticas_mapbiomas_c11_ucs.csv"

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Unidade', 'Categoria', 'Ano', 'ID_Classe', 'Nome_Classe', 'Cor_Hex', 'Pixels', 'Area_ha', 'Percentual'])
        for uc in resultados:
            for ano_str, ano_info in uc["anos"].items():
                for cl in ano_info["classes"]:
                    writer.writerow([
                        uc["unidade"],
                        uc["categoria"],
                        ano_info["ano"],
                        cl["id"],
                        cl["nome"],
                        cl["hex"],
                        cl["pixels"],
                        f"{cl['area_ha']:.2f}".replace('.', ','),
                        f"{cl['percentual']:.2f}%".replace('.', ',')
                    ])

    print("\n================================================================================")
    print(f"[SUCESSO] Estatísticas salvas com sucesso em:")
    print(f" -> {json_path}")
    print(f" -> {csv_path}")
    print("================================================================================")

    # Imprimir resumo no terminal
    for uc in resultados:
        print(f"\n================================================================================")
        print(f"UNIDADE: {uc['unidade']} ({uc['categoria']})")
        print("================================================================================")
        for ano in [1985, 1995, 2005, 2015, 2024]:
            ano_info = uc["anos"].get(str(ano))
            if not ano_info:
                continue
            print(f"\n--- ANO {ano} (Área Total: {ano_info['area_total_ha']:,.2f} ha) ---")
            for cl in ano_info["classes"]:
                bar = "#" * int(cl['percentual'] / 2)
                print(f"  {cl['id']:2d} | {cl['nome']:<30} | {cl['area_ha']:10,.2f} ha | {cl['percentual']:5.2f}% | {bar}")

calcular()

if app_iniciada:
    qgs_app.exitQgis()
