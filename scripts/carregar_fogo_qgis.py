# -*- coding: utf-8 -*-
"""
Script PyQGIS: Carregamento e Simbologia de Camadas de Fogo no QGIS
Projeto: REVIS Tabuleiro do Embaubal e RDS Vitória de Souzel

Execução:
Cole e execute este script no Console Python do QGIS (Ctrl + Alt + P)
ou via menu Plugins > Console Python > Executar Script.

O script realiza:
1. Localização automática do grupo '08. QUEIMADAS'.
2. Adição das camadas agrupadas por intervalo decadal:
   - Cicatrizes de Fogo (1985 – 1994) [Âmbar #F39C12]
   - Cicatrizes de Fogo (1995 – 2004) [Laranja Queimado #E67E22]
   - Cicatrizes de Fogo (2005 – 2014) [Vermelho Escarlate #E74C3C]
   - Cicatrizes de Fogo (2015 – 2024) [Carmim Bordeaux #900C3F]
   - Zona de Amortecimento (Buffer 2 km) [Linha Tracejada]
3. Aplicação de transparência e contorno profissional.
4. Definição do CRS SIRGAS 2000 (EPSG:4674) e ordenação visual ideal.
"""

import os
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFillSymbol,
    QgsSingleSymbolRenderer,
    QgsCoordinateReferenceSystem
)
from PyQt5.QtGui import QColor

def carregar_camadas_fogo():
    projeto = QgsProject.instance()
    root = projeto.layerTreeRoot()
    
    # 1. Localiza ou cria o grupo '08. QUEIMADAS'
    grupo_fogo = root.findGroup("08. QUEIMADAS")
    if not grupo_fogo:
        grupo_fogo = root.addGroup("08. QUEIMADAS")
        print("[+] Grupo '08. QUEIMADAS' criado na Árvore de Camadas.")
    else:
        print("[i] Grupo '08. QUEIMADAS' localizado.")

    # Diretório base relativo ao arquivo do projeto
    dir_proj = projeto.homePath()
    if not dir_proj:
        dir_proj = os.getcwd()

    camadas_config = [
        {
            "nome": "Cicatrizes de Fogo (2015 – 2024)",
            "path": os.path.join(dir_proj, "camadas", "mapbiomas-fogo", "agrupado", "fogo_2015_2024.shp"),
            "fill": QColor(144, 12, 63, 190),     # #900C3F 75% opacidade
            "stroke": QColor(88, 24, 69, 255),    # #581845
            "width": "0.3"
        },
        {
            "nome": "Cicatrizes de Fogo (2005 – 2014)",
            "path": os.path.join(dir_proj, "camadas", "mapbiomas-fogo", "agrupado", "fogo_2005_2014.shp"),
            "fill": QColor(231, 76, 60, 180),     # #E74C3C 70% opacidade
            "stroke": QColor(146, 43, 33, 255),   # #922B21
            "width": "0.3"
        },
        {
            "nome": "Cicatrizes de Fogo (1995 – 2004)",
            "path": os.path.join(dir_proj, "camadas", "mapbiomas-fogo", "agrupado", "fogo_1995_2004.shp"),
            "fill": QColor(230, 126, 34, 180),    # #E67E22 70% opacidade
            "stroke": QColor(160, 64, 0, 255),    # #A04000
            "width": "0.3"
        },
        {
            "nome": "Cicatrizes de Fogo (1985 – 1994)",
            "path": os.path.join(dir_proj, "camadas", "mapbiomas-fogo", "agrupado", "fogo_1985_1994.shp"),
            "fill": QColor(243, 156, 18, 180),    # #F39C12 70% opacidade
            "stroke": QColor(185, 119, 14, 255),  # #B9770E
            "width": "0.3"
        },
        {
            "nome": "Zona de Amortecimento (Buffer 2 km UCs)",
            "path": os.path.join(dir_proj, "camadas", "mapbiomas-fogo", "Buffer_Externo_2km_UCs.shp"),
            "fill": QColor(0, 0, 0, 0),           # Transparente
            "stroke": QColor(192, 57, 43, 220),   # Vermelho borda
            "width": "0.6",
            "style": "dash"
        }
    ]

    crs_padrao = QgsCoordinateReferenceSystem("EPSG:4674")

    for cfg in camadas_config:
        fpath = cfg["path"]
        nome = cfg["nome"]

        if not os.path.exists(fpath):
            print(f"[!] Arquivo não encontrado: {fpath}")
            continue

        # Evita duplicação se a camada já estiver carregada
        existentes = projeto.mapLayersByName(nome)
        if existentes:
            print(f"[i] Camada '{nome}' já existe no projeto. Atualizando estilo...")
            layer = existentes[0]
        else:
            layer = QgsVectorLayer(fpath, nome, "ogr")
            if not layer.isValid():
                print(f"[!] Falha ao carregar {fpath}")
                continue
            
            layer.setCrs(crs_padrao)
            projeto.addMapLayer(layer, False)
            grupo_fogo.addLayer(layer)
            print(f"[+] Camada adicionada ao grupo: {nome}")

        # Configuração do Símbolo
        props = {
            "color": f"{cfg['fill'].red()},{cfg['fill'].green()},{cfg['fill'].blue()},{cfg['fill'].alpha()}",
            "outline_color": f"{cfg['stroke'].red()},{cfg['stroke'].green()},{cfg['stroke'].blue()},{cfg['stroke'].alpha()}",
            "outline_width": cfg["width"],
            "outline_width_unit": "MM",
            "style": "solid" if cfg["fill"].alpha() > 0 else "no"
        }
        if cfg.get("style") == "dash":
            props["outline_style"] = "dash"
        else:
            props["outline_style"] = "solid"

        symbol = QgsFillSymbol.createSimple(props)
        renderer = QgsSingleSymbolRenderer(symbol)
        layer.setRenderer(renderer)
        layer.triggerRepaint()

    print("\n[SUCESSO] Todas as camadas do Tema Fogo foram configuradas no QGIS com sucesso!")

carregar_camadas_fogo()
