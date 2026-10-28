# -*- coding: utf-8 -*-
"""
===============================================================================
Estilização Oficial MapBiomas Brasil - Coleção 11 (PyQGIS)
===============================================================================
Script universal e portável para QGIS 3.x e 4.x.
Não depende de caminhos locais ou absolutos. Funciona em qualquer computador
e com qualquer projeto aberto.

Modos de Operação:
1. Se houver camadas raster selecionadas no painel: estiliza as camadas selecionadas.
2. Se nenhuma estiver selecionada: busca automaticamente no projeto camadas raster
   do MapBiomas e as estiliza.
3. Se a camada for multibandas (ex: série temporal):
   - Estiliza a banda ativa/recente.
   - Cria/organiza as bandas temporais em camadas individuais na árvore do projeto.
4. Filtro inteligente: inclui na legenda apenas as classes que realmente possuem
   pixels no recorte, mantendo a legenda do layout limpa e técnica.
===============================================================================
"""

try:
    from PyQt6.QtGui import QColor
except ImportError:
    from PyQt5.QtGui import QColor

from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsPalettedRasterRenderer,
    QgsRasterBandStats
)
from qgis.utils import iface

# TABELA OFICIAL DE CLASSES E CORES - MAPBIOMAS COLEÇÃO 11
CLASSES_MAPBIOMAS_C11 = {
    1:  {'hex': '#1f8d49', 'nome': '1. Floresta'},
    3:  {'hex': '#1f8d49', 'nome': '1.1. Formação Florestal'},
    6:  {'hex': '#007785', 'nome': '1.2. Floresta Alagável'},
    4:  {'hex': '#7dc975', 'nome': '1.3. Formação Savânica'},
    7:  {'hex': '#228c70', 'nome': '1.4. Savana Alagada (beta)'},
    5:  {'hex': '#04381d', 'nome': '1.5. Mangue'},
    49: {'hex': '#02d659', 'nome': '1.6. Restinga Arbórea'},
    10: {'hex': '#d6bc74', 'nome': '2. Vegetação Herbácea e Arbustiva'},
    12: {'hex': '#d6bc74', 'nome': '2.1. Formação Campestre'},
    77: {'hex': '#86b074', 'nome': '2.2. Formação Herbáceo Arbustiva'},
    11: {'hex': '#519799', 'nome': '2.3. Campo Alagado e Área Pantanosa'},
    84: {'hex': '#81dbbf', 'nome': '2.4. Marisma (beta)'},
    50: {'hex': '#ffaa5f', 'nome': '2.5. Restinga Herbácea ou Arbustiva'},
    32: {'hex': '#fc8114', 'nome': '2.6. Apicum'},
    29: {'hex': '#ad5100', 'nome': '2.7. Afloramento Rochoso'},
    14: {'hex': '#ffefc3', 'nome': '3. Agropecuária'},
    15: {'hex': '#edde8e', 'nome': '3.1. Pastagem'},
    18: {'hex': '#E974ED', 'nome': '3.2. Agricultura'},
    19: {'hex': '#C27BA0', 'nome': '3.2.1. Lavoura Temporária'},
    39: {'hex': '#f5b3c8', 'nome': '3.2.1.1. Soja'},
    20: {'hex': '#db7093', 'nome': '3.2.1.2. Cana'},
    40: {'hex': '#c71585', 'nome': '3.2.1.3. Arroz'},
    62: {'hex': '#ff69b4', 'nome': '3.2.1.4. Algodão (beta)'},
    41: {'hex': '#f54ca9', 'nome': '3.2.1.5. Outras Lavouras Temporárias'},
    36: {'hex': '#d082de', 'nome': '3.2.2. Lavoura Perene'},
    46: {'hex': '#d68fe2', 'nome': '3.2.2.1. Café'},
    47: {'hex': '#9932cc', 'nome': '3.2.2.2. Citrus'},
    35: {'hex': '#9065d0', 'nome': '3.2.2.3. Dendê'},
    48: {'hex': '#e6ccff', 'nome': '3.2.2.4. Outras Lavouras Perenes'},
    9:  {'hex': '#7a5900', 'nome': '3.3. Silvicultura'},
    21: {'hex': '#ffefc3', 'nome': '3.4. Mosaico de Usos'},
    22: {'hex': '#d4271e', 'nome': '4. Área não Vegetada'},
    23: {'hex': '#ffa07a', 'nome': '4.1. Praia, Duna e Areal'},
    24: {'hex': '#d4271e', 'nome': '4.2. Área Urbanizada'},
    30: {'hex': '#9c0027', 'nome': '4.3. Mineração'},
    75: {'hex': '#757272', 'nome': '4.4. Usina Fotovoltaica'},
    91: {'hex': '#403d3e', 'nome': '4.5. Parque Eólico (beta)'},
    25: {'hex': '#db4d4f', 'nome': '4.6. Outras Áreas não Vegetadas'},
    26: {'hex': '#2532e4', 'nome': '5. Corpo D\'Água'},
    33: {'hex': '#2532e4', 'nome': '5.1. Rio, Lago e Oceano'},
    31: {'hex': '#091077', 'nome': '5.2. Aquicultura'},
    27: {'hex': '#ffffff', 'nome': 'Não Observado'}
}

# Rótulos para bandas temporais padrão (se for stack de 5 bandas)
ROTULOS_5_BANDAS = {
    1: "1985",
    2: "1995",
    3: "2005",
    4: "2015",
    5: "2024"
}

def obter_classes_existentes(layer, banda=1):
    """Analisa os pixels do raster e retorna os IDs únicos presentes."""
    provider = layer.dataProvider()
    block = provider.block(banda, layer.extent(), layer.width(), layer.height())
    valores = set()
    w = layer.width()
    h = layer.height()
    step_x = max(1, w // 400)
    step_y = max(1, h // 400)
    
    for y in range(0, h, step_y):
        for x in range(0, w, step_x):
            if not block.isNoData(y, x):
                v = int(block.value(y, x))
                if v > 0:
                    valores.add(v)
    return sorted(list(valores))

def construir_renderer_paletizado(layer, banda=1, filtrar_existentes=True):
    """Cria o QgsPalettedRasterRenderer oficial MapBiomas C11."""
    provider = layer.dataProvider()
    classes_palette = []
    
    if filtrar_existentes:
        ids_presentes = obter_classes_existentes(layer, banda)
        if not ids_presentes:
            ids_presentes = list(CLASSES_MAPBIOMAS_C11.keys())
    else:
        ids_presentes = list(CLASSES_MAPBIOMAS_C11.keys())

    for cid in ids_presentes:
        if cid in CLASSES_MAPBIOMAS_C11:
            info = CLASSES_MAPBIOMAS_C11[cid]
            c = QgsPalettedRasterRenderer.Class(cid, QColor(info['hex']), info['nome'])
            classes_palette.append(c)
        else:
            c = QgsPalettedRasterRenderer.Class(cid, QColor("#808080"), f"Classe {cid}")
            classes_palette.append(c)

    return QgsPalettedRasterRenderer(provider, banda, classes_palette)

def estilizar_raster(layer, banda=1, filtrar_existentes=True):
    """Aplica simbologia e força atualização visual."""
    if not layer or not isinstance(layer, QgsRasterLayer) or not layer.isValid():
        return False
    
    renderer = construir_renderer_paletizado(layer, banda, filtrar_existentes)
    layer.setRenderer(renderer)
    layer.triggerRepaint()
    
    if iface:
        iface.layerTreeView().refreshLayerSymbology(layer.id())
    
    print(f"  -> Camada '{layer.name()}' estilizada com sucesso (Banda {banda}).")
    return True

def executar():
    """Identifica camadas ativas/selecionadas ou do projeto e aplica o estilo."""
    projeto = QgsProject.instance()
    camadas_alvo = []
    
    # 1. Verifica se há camadas selecionadas pelo usuário na árvore
    if iface:
        selecionadas = [l for l in iface.layerTreeView().selectedLayers() if isinstance(l, QgsRasterLayer)]
        if selecionadas:
            camadas_alvo = selecionadas
            print(f"[MODO] Estilizando {len(camadas_alvo)} camada(s) selecionada(s) no painel.")

    # 2. Se nenhuma foi selecionada, procura camadas do MapBiomas no projeto
    if not camadas_alvo:
        for l in projeto.mapLayers().values():
            if isinstance(l, QgsRasterLayer):
                texto = (l.name() + " " + l.source()).lower()
                if 'mapbiomas' in texto:
                    camadas_alvo.append(l)
        if camadas_alvo:
            print(f"[MODO] Encontradas {len(camadas_alvo)} camada(s) MapBiomas carregadas no projeto.")

    # 3. Fallback: usa a camada ativa se for raster
    if not camadas_alvo and iface and iface.activeLayer() and isinstance(iface.activeLayer(), QgsRasterLayer):
        camadas_alvo = [iface.activeLayer()]
        print(f"[MODO] Usando camada raster ativa: '{iface.activeLayer().name()}'.")

    if not camadas_alvo:
        print("[ERRO] Nenhuma camada raster encontrada. Selecione a camada do MapBiomas no painel e execute novamente.")
        return

    root = projeto.layerTreeRoot()

    for layer in camadas_alvo:
        band_count = layer.bandCount()
        
        # Caso Multibandas (série temporal)
        if band_count > 1:
            print(f"\n[MULTIBANDAS] '{layer.name()}' possui {band_count} bandas.")
            # Estiliza o raster original na última banda
            estilizar_raster(layer, banda=band_count, filtrar_existentes=True)
            
            # Cria grupo temporal desdobrado usando o próprio layer.source() existente
            grupo_nome = f"Série Temporal - {layer.name()}"
            grupo = root.findGroup(grupo_nome) or root.addGroup(grupo_nome)
            
            for b_idx in range(1, band_count + 1):
                rotulo_ano = ROTULOS_5_BANDAS.get(b_idx, f"Ano/Banda {b_idx}")
                sub_nome = f"{layer.name()} ({rotulo_ano})"
                
                # Procura se já foi criada
                sub_layer = None
                for node in grupo.children():
                    if node.name() == sub_nome:
                        sub_layer = node.layer()
                        break
                
                if not sub_layer:
                    sub_layer = QgsRasterLayer(layer.source(), sub_nome)
                    if sub_layer.isValid():
                        projeto.addMapLayer(sub_layer, False)
                        grupo.addLayer(sub_layer)
                
                if sub_layer and sub_layer.isValid():
                    estilizar_raster(sub_layer, banda=b_idx, filtrar_existentes=True)
                    node = grupo.findLayer(sub_layer.id())
                    if node:
                        node.setItemVisibilityChecked(b_idx == band_count)
            print(f"  [+] Grupo '{grupo_nome}' criado com as {band_count} bandas prontas para comparação!")
        
        # Caso Banda Única
        else:
            estilizar_raster(layer, banda=1, filtrar_existentes=True)

    if iface:
        iface.mapCanvas().refreshAllLayers()
        iface.mapCanvas().redrawAllLayers()

    print("\n[CONCLUÍDO] Simbologia aplicada e tela atualizada com sucesso!\n")

# Executa
executar()
