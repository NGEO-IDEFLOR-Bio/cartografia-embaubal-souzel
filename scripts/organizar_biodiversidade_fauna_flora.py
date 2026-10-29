# -*- coding: utf-8 -*-
"""
Classificação, Higienização Toponímica e Estruturação Temática de Biodiversidade:
Resolve o problema de misturar peixes, botos, santuários e árvores matrizes na camada 08.

Atribui:
- grupo_macro (para categorização no QGIS)
- grupo_tematico
- tipo_feicao
- nome_padronizado (toponímia formal e técnica)
- icone_sugerido (dolphin, fish, turtle, tree, sanctuary, livestock, water)
"""

import os
import json
import zipfile
import xml.etree.ElementTree as ET
import geopandas as gpd
import pandas as pd

FPATH_FLORA = "camadas/08_vegetacao_e_flora.geojson"
DIR_BIO = "camadas/biodiversidade"
QGZ_PATH = "tabuleiro_do_embaubal_e_vitoria_souzel.qgz"

os.makedirs(DIR_BIO, exist_ok=True)

# 1. Carrega camada original
gdf = gpd.read_file(FPATH_FLORA)
print(f"Total de feições carregadas: {len(gdf)}")

# Dicionário de classificação analítica dos 44 pontos
MAPA_ATRIBUTOS = {
    # --- FAUNA AQUÁTICA E PESCA ---
    581: {
        'grupo_macro': 'Fauna Aquática e Pesca',
        'grupo_tematico': 'Mamíferos Aquáticos',
        'tipo_feicao': 'Ponto de Avistamento de Botos',
        'nome': 'Ponto de Avistamento de Botos',
        'subcategoria': 'Mamíferos Aquáticos (Botos)',
        'icone': './simbologia/ian-symbols/Fauna/Mammals/tursiops-spp-bottlenose-dolphin.svg',
        'cor': '#00a8ff'  # Azul Ciano
    },
    586: {
        'grupo_macro': 'Fauna Aquática e Pesca',
        'grupo_tematico': 'Ictiofauna / Reprodução',
        'tipo_feicao': 'Área de Piracema',
        'nome': 'Área de Piracema (Curimatã)',
        'subcategoria': 'Ictiofauna (Reprodução / Piracema)',
        'icone': './simbologia/ian-symbols/Fauna/Fish/acanthurus-achilles-achilles-tang.svg',
        'cor': '#0984e3'
    },
    121: {
        'grupo_macro': 'Fauna Aquática e Pesca',
        'grupo_tematico': 'Ictiofauna / Berçário',
        'tipo_feicao': 'Berçário Aquático',
        'nome': 'Berçário Natural de Peixes',
        'subcategoria': 'Berçários Naturais',
        'icone': './simbologia/ian-symbols/Fauna/Fish/acanthurus-achilles-achilles-tang.svg',
        'cor': '#0984e3'
    },
    122: {
        'grupo_macro': 'Fauna Aquática e Pesca',
        'grupo_tematico': 'Ictiofauna e Mamíferos Aquáticos',
        'tipo_feicao': 'Berçário de Pirarucu e Peixe-Boi',
        'nome': 'Berçário de Pirarucu e Peixe-Boi',
        'subcategoria': 'Espécies Ameaçadas (Pirarucu / Peixe-Boi)',
        'icone': './simbologia/ian-symbols/Fauna/Fish/acanthurus-achilles-achilles-tang.svg',
        'cor': '#0984e3'
    },
    123: {
        'grupo_macro': 'Fauna Aquática e Pesca',
        'grupo_tematico': 'Ictiofauna / Berçário',
        'tipo_feicao': 'Berçário de Pirarucu',
        'nome': 'Berçário Natural de Pirarucu',
        'subcategoria': 'Ictiofauna (Pirarucu)',
        'icone': './simbologia/ian-symbols/Fauna/Fish/acanthurus-achilles-achilles-tang.svg',
        'cor': '#0984e3'
    },
    126: {
        'grupo_macro': 'Fauna Aquática e Pesca',
        'grupo_tematico': 'Mamíferos Aquáticos',
        'tipo_feicao': 'Boiador de Peixe-Boi',
        'nome': 'Boiador de Peixe-Boi',
        'subcategoria': 'Mamíferos Aquáticos (Peixe-Boi)',
        'icone': './simbologia/ian-symbols/Fauna/Mammals/tursiops-spp-bottlenose-dolphin.svg',
        'cor': '#00a8ff'
    },
    304: {
        'grupo_macro': 'Fauna Aquática e Pesca',
        'grupo_tematico': 'Mamíferos Aquáticos / Alimentação',
        'tipo_feicao': 'Pastagem de Peixe-Boi',
        'nome': 'Área de Alimentação de Peixe-Boi (Pastagem)',
        'subcategoria': 'Alimentação de Fauna Aquática',
        'icone': './simbologia/ian-symbols/Fauna/Mammals/tursiops-spp-bottlenose-dolphin.svg',
        'cor': '#00a8ff'
    },
    305: {
        'grupo_macro': 'Fauna Aquática e Pesca',
        'grupo_tematico': 'Mamíferos Aquáticos / Alimentação',
        'tipo_feicao': 'Pastagem de Peixe-Boi',
        'nome': 'Área de Alimentação de Peixe-Boi (Pastagem)',
        'subcategoria': 'Alimentação de Fauna Aquática',
        'icone': './simbologia/ian-symbols/Fauna/Mammals/tursiops-spp-bottlenose-dolphin.svg',
        'cor': '#00a8ff'
    },
    567: {
        'grupo_macro': 'Fauna Aquática e Pesca',
        'grupo_tematico': 'Mamíferos Aquáticos',
        'tipo_feicao': 'Área de Peixe-Boi',
        'nome': 'Área de Ocorrência Relevante de Peixe-Boi',
        'subcategoria': 'Mamíferos Aquáticos (Peixe-Boi)',
        'icone': './simbologia/ian-symbols/Fauna/Mammals/tursiops-spp-bottlenose-dolphin.svg',
        'cor': '#00a8ff'
    },
    587: {
        'grupo_macro': 'Fauna Aquática e Pesca',
        'grupo_tematico': 'Aquicultura Tradicional',
        'tipo_feicao': 'Tanque-Rede',
        'nome': 'Área de Piscicultura (Tanque-Rede)',
        'subcategoria': 'Manejo / Aquicultura',
        'icone': './simbologia/ian-symbols/Fauna/Fish/acanthurus-achilles-achilles-tang.svg',
        'cor': '#0984e3'
    },

    # --- QUELÔNIOS E RÉPTEIS ---
    125: {
        'grupo_macro': 'Quelônios e Répteis',
        'grupo_tematico': 'Quelônios',
        'tipo_feicao': 'Boiadeiro de Tartarugas',
        'nome': 'Boiadeiro de Tartarugas',
        'subcategoria': 'Quelônios (Tartaruga/Tracajá)',
        'icone': './simbologia/ian-symbols/Fauna/Reptiles/caretta-caretta-loggerhead-turtle.svg',
        'cor': '#00b894'  # Verde Esmeralda
    },
    153: {
        'grupo_macro': 'Quelônios e Répteis',
        'grupo_tematico': 'Quelônios',
        'tipo_feicao': 'Concentração de Tartarugas',
        'nome': 'Área de Concentração de Tartarugas',
        'subcategoria': 'Quelônios (Tartaruga/Tracajá)',
        'icone': './simbologia/ian-symbols/Fauna/Reptiles/caretta-caretta-loggerhead-turtle.svg',
        'cor': '#00b894'
    },
    154: {
        'grupo_macro': 'Quelônios e Répteis',
        'grupo_tematico': 'Quelônios',
        'tipo_feicao': 'Concentração de Tartarugas',
        'nome': 'Área de Concentração de Tartarugas',
        'subcategoria': 'Quelônios (Tartaruga/Tracajá)',
        'icone': './simbologia/ian-symbols/Fauna/Reptiles/caretta-caretta-loggerhead-turtle.svg',
        'cor': '#00b894'
    },
    155: {
        'grupo_macro': 'Quelônios e Répteis',
        'grupo_tematico': 'Quelônios',
        'tipo_feicao': 'Concentração de Tartarugas',
        'nome': 'Área de Concentração de Tartarugas',
        'subcategoria': 'Quelônios (Tartaruga/Tracajá)',
        'icone': './simbologia/ian-symbols/Fauna/Reptiles/caretta-caretta-loggerhead-turtle.svg',
        'cor': '#00b894'
    },
    294: {
        'grupo_macro': 'Quelônios e Répteis',
        'grupo_tematico': 'Quelônios / Ninhos',
        'tipo_feicao': 'Ninho de Pitiú',
        'nome': 'Sítio de Ninho de Pitiú',
        'subcategoria': 'Quelônios (Ninhos)',
        'icone': './simbologia/ian-symbols/Fauna/Reptiles/caretta-caretta-loggerhead-turtle.svg',
        'cor': '#00b894'
    },
    295: {
        'grupo_macro': 'Quelônios e Répteis',
        'grupo_tematico': 'Quelônios / Ninhos',
        'tipo_feicao': 'Ninho de Pitiú',
        'nome': 'Sítio de Ninho de Pitiú',
        'subcategoria': 'Quelônios (Ninhos)',
        'icone': './simbologia/ian-symbols/Fauna/Reptiles/caretta-caretta-loggerhead-turtle.svg',
        'cor': '#00b894'
    },
    325: {
        'grupo_macro': 'Quelônios e Répteis',
        'grupo_tematico': 'Quelônios / Tabuleiros',
        'tipo_feicao': 'Tabuleiro de Desova',
        'nome': 'Potencial Tabuleiro de Desova de Tartaruga',
        'subcategoria': 'Quelônios (Tabuleiros de Desova)',
        'icone': './simbologia/ian-symbols/Fauna/Reptiles/caretta-caretta-loggerhead-turtle.svg',
        'cor': '#00b894'
    },
    432: {
        'grupo_macro': 'Quelônios e Répteis',
        'grupo_tematico': 'Quelônios / Migração',
        'tipo_feicao': 'Rota de Tartarugas',
        'nome': 'Rota Migratória de Tartarugas',
        'subcategoria': 'Quelônios (Rotas Migratórias)',
        'icone': './simbologia/ian-symbols/Fauna/Reptiles/caretta-caretta-loggerhead-turtle.svg',
        'cor': '#00b894'
    },
    470: {
        'grupo_macro': 'Quelônios e Répteis',
        'grupo_tematico': 'Quelônios',
        'tipo_feicao': 'Concentração de Tracajás',
        'nome': 'Área de Abundância de Tracajá e Tartaruga',
        'subcategoria': 'Quelônios (Tartaruga/Tracajá)',
        'icone': './simbologia/ian-symbols/Fauna/Reptiles/caretta-caretta-loggerhead-turtle.svg',
        'cor': '#00b894'
    },
    500: {
        'grupo_macro': 'Quelônios e Répteis',
        'grupo_tematico': 'Quelônios',
        'tipo_feicao': 'Ocorrência de Tracajás',
        'nome': 'Lago do Palhal (Ocorrência de Tracajás)',
        'subcategoria': 'Quelônios (Tartaruga/Tracajá)',
        'icone': './simbologia/ian-symbols/Fauna/Reptiles/caretta-caretta-loggerhead-turtle.svg',
        'cor': '#00b894'
    },
    412: {
        'grupo_macro': 'Quelônios e Répteis',
        'grupo_tematico': 'Répteis / Jacarés',
        'tipo_feicao': 'Reprodução de Jacaré',
        'nome': 'Sítio de Reprodução de Jacaré',
        'subcategoria': 'Répteis (Jacarés)',
        'icone': './simbologia/ian-symbols/Fauna/Reptiles/chelydra-serpentina-snapping-turtle.svg',
        'cor': '#00b894'
    },

    # --- SANTUÁRIOS E ÁREAS DE REFÚGIO DA BIODIVERSIDADE ---
    434: {
        'grupo_macro': 'Santuários e Refúgios de Fauna',
        'grupo_tematico': 'Refúgio de Fauna',
        'tipo_feicao': 'Santuário de Animais',
        'nome': 'Santuário de Fauna Silvestre',
        'subcategoria': 'Áreas de Refúgio e Proteção Integral',
        'icone': './simbologia/maki/star.svg',
        'cor': '#f39c12'  # Âmbar Dourado
    },
    435: {
        'grupo_macro': 'Santuários e Refúgios de Fauna',
        'grupo_tematico': 'Refúgio Multiespécie',
        'tipo_feicao': 'Santuário de Animais',
        'nome': 'Santuário de Tartaruga, Peixe-Boi e Pirarucu',
        'subcategoria': 'Áreas de Refúgio e Proteção Integral',
        'icone': './simbologia/maki/star.svg',
        'cor': '#f39c12'
    },
    72: {
        'grupo_macro': 'Santuários e Refúgios de Fauna',
        'grupo_tematico': 'Fauna Terrestre',
        'tipo_feicao': 'Ocorrência de Cutia',
        'nome': 'Ponto de Avistamento de Cutia',
        'subcategoria': 'Fauna Terrestre (Mamíferos)',
        'icone': './simbologia/maki/star.svg',
        'cor': '#f39c12'
    },

    # --- FLORA NATIVA, EXTRATIVISMO E ÁRVORES MATRIZES ---
    499: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Árvores Matrizes',
        'tipo_feicao': 'Jatobá Matriz',
        'nome': 'Jatobá Matriz (Hymenaea courbaril)',
        'subcategoria': 'Árvores Matrizes',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'  # Verde Floresta
    },
    555: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Extrativismo / Seringueira',
        'tipo_feicao': 'Seringueira Matriz',
        'nome': 'Seringueira Matriz (Lanhada)',
        'subcategoria': 'Seringueiras Matrizes',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'
    },
    69: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Extrativismo / Seringueira',
        'tipo_feicao': 'Seringueira Lanhada',
        'nome': 'Seringueira com Extração Tradicional (Lanhada)',
        'subcategoria': 'Seringueiras Matrizes',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'
    },
    21: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Extrativismo / Seringal',
        'tipo_feicao': 'Seringal Nativo',
        'nome': 'Seringal Nativo da RDS',
        'subcategoria': 'Seringais Nativos',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'
    },
    471: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Extrativismo / Seringal',
        'tipo_feicao': 'Ocorrência de Seringueiras',
        'nome': 'Ocorrência de Seringueiras Nativas',
        'subcategoria': 'Seringais Nativos',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'
    },
    478: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Histórico / Extrativismo',
        'tipo_feicao': 'Antigo Seringal',
        'nome': 'Antigo Seringal Histórico',
        'subcategoria': 'Seringais Nativos',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'
    },
    453: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Flora Ribeirinha / Embaúbas',
        'tipo_feicao': 'Embaubal Nativo',
        'nome': 'Formação Típica de Embaubal (Cecropia spp.)',
        'subcategoria': 'Vegetação Ribeirinha',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'
    },
    310: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Frutíferas Nativas',
        'tipo_feicao': 'Pitanguinha',
        'nome': 'Ocorrência de Pitanguinha Nativa',
        'subcategoria': 'Frutíferas Silvestres',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'
    },
    311: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Agrofloresta Tradicional',
        'tipo_feicao': 'Plantio de Cacau',
        'nome': 'Área de Plantio Tradicional de Cacau',
        'subcategoria': 'Sistemas Agroflorestais',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'
    },
    36: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Cobertura Florestal',
        'tipo_feicao': 'Mata Nativa',
        'nome': 'Mata de Várzea Preservada',
        'subcategoria': 'Formações Florestais',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'
    },
    26: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Cobertura Arbórea',
        'tipo_feicao': 'Árvores Secas',
        'nome': 'Formação Arbórea Natural (Árvores Secas)',
        'subcategoria': 'Formações Florestais',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'
    },
    105: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Campos Naturais',
        'tipo_feicao': 'Campos Alagáveis',
        'nome': 'Formação de Campos Naturais Alagáveis',
        'subcategoria': 'Campos Naturais',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'
    },
    590: {
        'grupo_macro': 'Flora e Árvores Matrizes',
        'grupo_tematico': 'Mata Comunitária',
        'tipo_feicao': 'Reserva Comunitária',
        'nome': 'Mata Preservada da Comunidade (Cercada)',
        'subcategoria': 'Conservação Comunitária',
        'icone': './simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg',
        'cor': '#27ae60'
    },

    # --- USOS TRADICIONAIS E MANEJO TERRITORIAL ---
    152: {
        'grupo_macro': 'Usos Tradicionais e Manejo',
        'grupo_tematico': 'Pecuária Tradicional',
        'tipo_feicao': 'Gado Bovino',
        'nome': 'Área de Concentração de Gado Bovino',
        'subcategoria': 'Manejo Pecuário',
        'icone': './simbologia/maki/circle.svg',
        'cor': '#e67e22'  # Laranja Terracota
    },
    585: {
        'grupo_macro': 'Usos Tradicionais e Manejo',
        'grupo_tematico': 'Pecuária Tradicional',
        'tipo_feicao': 'Manejo de Verão',
        'nome': 'Área de Manejo de Gado no Verão',
        'subcategoria': 'Manejo Pecuário',
        'icone': './simbologia/maki/circle.svg',
        'cor': '#e67e22'
    },
    589: {
        'grupo_macro': 'Usos Tradicionais e Manejo',
        'grupo_tematico': 'Pecuária Bubalina',
        'tipo_feicao': 'Criação de Búfalos',
        'nome': 'Área com Ocorrência de Búfalos',
        'subcategoria': 'Manejo Pecuário (Búfalos)',
        'icone': './simbologia/maki/circle.svg',
        'cor': '#e67e22'
    },
    479: {
        'grupo_macro': 'Usos Tradicionais e Manejo',
        'grupo_tematico': 'Referência Hídrica',
        'tipo_feicao': 'Braço do Meio',
        'nome': 'Braço do Meio (Referência Local)',
        'subcategoria': 'Hidrografia Local',
        'icone': './simbologia/maki/circle.svg',
        'cor': '#34495e'
    },
    480: {
        'grupo_macro': 'Usos Tradicionais e Manejo',
        'grupo_tematico': 'Referência Hídrica',
        'tipo_feicao': 'Braço do Meio',
        'nome': 'Braço do Meio (Extremidade)',
        'subcategoria': 'Hidrografia Local',
        'icone': './simbologia/maki/circle.svg',
        'cor': '#34495e'
    },
    487: {
        'grupo_macro': 'Usos Tradicionais e Manejo',
        'grupo_tematico': 'Infraestrutura Hidroviária',
        'tipo_feicao': 'Canal de Dragagem',
        'nome': 'Canal de Dragagem e Acesso Hidroviário',
        'subcategoria': 'Intervenção Hidroviária',
        'icone': './simbologia/maki/circle.svg',
        'cor': '#34495e'
    },
    566: {
        'grupo_macro': 'Usos Tradicionais e Manejo',
        'grupo_tematico': 'Manejo de Lagos',
        'tipo_feicao': 'Tapagem de Lagos',
        'nome': 'Tapagem Tradicional Divisória de Lagos',
        'subcategoria': 'Manejo Hídrico Tradicional',
        'icone': './simbologia/maki/circle.svg',
        'cor': '#34495e'
    }
}

# 2. Aplica as novas classificações
for idx, row in gdf.iterrows():
    nid = row['id']
    if nid in MAPA_ATRIBUTOS:
        cfg = MAPA_ATRIBUTOS[nid]
        gdf.loc[idx, 'grupo_macro'] = cfg['grupo_macro']
        gdf.loc[idx, 'grupo_tematico'] = cfg['grupo_tematico']
        gdf.loc[idx, 'tipo_feicao'] = cfg['tipo_feicao']
        gdf.loc[idx, 'nome'] = cfg['nome']
        gdf.loc[idx, 'categoria'] = 'Biodiversidade e Recursos Naturais'
        gdf.loc[idx, 'subcategoria'] = cfg['subcategoria']
        gdf.loc[idx, 'icone_sugerido'] = cfg['icone']
        gdf.loc[idx, 'cor_hex'] = cfg['cor']

# Salva arquivo principal atualizado
gdf.to_file(FPATH_FLORA, driver="GeoJSON", encoding="utf-8")
print(f"[OK] {FPATH_FLORA} atualizado com atributos enriquecidos!")

# 3. Exporta subcamadas temáticas na pasta camadas/biodiversidade/
for gname, sub in gdf.groupby('grupo_macro'):
    slug = gname.lower().replace(" ", "_").replace("ç", "c").replace("ã", "a").replace("é", "e").replace("á", "a").replace("/", "_").replace(",", "")
    out_path = f"{DIR_BIO}/{slug}.geojson"
    sub.to_file(out_path, driver="GeoJSON", encoding="utf-8")
    print(f"  + Subcamada criada: {out_path} ({len(sub)} pontos)")

# 4. Atualiza o consolidado geral
print("\n--- Atualizando consolidado de pontos ---")
camadas_ativas = [
    '01_moradores_e_comunidades.geojson',
    '02_apoio_de_pesca_e_ranchos.geojson',
    '03_areas_de_desova.geojson',
    '04_hidrografia.geojson',
    '05_ilhas_e_praias.geojson',
    '06_infraestrutura_e_equipamentos.geojson',
    '07_marcos_e_pontos_referencia.geojson',
    '08_vegetacao_e_flora.geojson',
    '09_ocorrencias_e_impactos.geojson',
    '10_trajetos_e_acessos.geojson'
]

gdfs = [gpd.read_file(f"camadas/{c}").to_crs(epsg=4674) for c in camadas_ativas if os.path.exists(f"camadas/{c}") and len(gpd.read_file(f"camadas/{c}")) > 0]
gdf_cons = pd.concat(gdfs, ignore_index=True)
gdf_cons = gpd.GeoDataFrame(gdf_cons, geometry='geometry', crs="EPSG:4674")

gdf_cons.to_file("camadas/pontos_revis_rds_consolidado.geojson", driver="GeoJSON", encoding="utf-8")
gdf_cons.to_file("camadas/pontos_revis_rds_consolidado.gpkg", layer="pontos_campo", driver="GPKG")
print(f"[OK] Consolidado atualizado: {len(gdf_cons)} pontos.")

# -------------------------------------------------------------
# 5. ATUALIZAÇÃO NO PROJETO QGIS (.QGZ)
# Aplica categorização oficial por grupo_macro na camada
# -------------------------------------------------------------
print("\n--- Atualizando simbologia no QGZ (Categorização Inteligente) ---")

with zipfile.ZipFile(QGZ_PATH, 'r') as z:
    qgs_bytes = z.read("tabuleiro_do_embaubal_e_vitoria_souzel.qgs")
    outras_partes = {n: z.read(n) for n in z.namelist() if n != "tabuleiro_do_embaubal_e_vitoria_souzel.qgs"}

root = ET.fromstring(qgs_bytes)

# Definição dos 5 símbolos categorizados
CATEGORIAS = [
    {
        "valor": "Fauna Aquática e Pesca",
        "label": "Fauna Aquática (Botos, Peixe-Boi, Piracema, Pirarucu)",
        "cor_bg": "0,168,255,255",        # Azul Ciano
        "border": "9,132,227,255",
        "icon": "./simbologia/ian-symbols/Fauna/Mammals/tursiops-spp-bottlenose-dolphin.svg",
        "size_bg": "7.5",
        "size_icon": "5.5"
    },
    {
        "valor": "Quelônios e Répteis",
        "label": "Quelônios e Répteis (Tartarugas, Tracajás, Jacarés)",
        "cor_bg": "0,184,148,255",        # Verde Esmeralda
        "border": "0,127,95,255",
        "icon": "./simbologia/ian-symbols/Fauna/Reptiles/caretta-caretta-loggerhead-turtle.svg",
        "size_bg": "7.5",
        "size_icon": "5.5"
    },
    {
        "valor": "Flora e Árvores Matrizes",
        "label": "Flora e Extrativismo (Seringais, Jatobás, Matas)",
        "cor_bg": "39,174,96,255",        # Verde Floresta
        "border": "27,54,38,255",
        "icon": "./simbologia/ian-symbols/Flora/Trees, Shrubs, Vines/acacia-koa-koa-tree.svg",
        "size_bg": "7.5",
        "size_icon": "5.5"
    },
    {
        "valor": "Santuários e Refúgios de Fauna",
        "label": "Santuários e Refúgios de Fauna Silvestre",
        "cor_bg": "243,156,18,255",       # Dourado Âmbar
        "border": "185,119,14,255",
        "icon": "./simbologia/maki/star.svg",
        "size_bg": "8.5",
        "size_icon": "6.0"
    },
    {
        "valor": "Usos Tradicionais e Manejo",
        "label": "Manejo Territorial e Usos Tradicionais",
        "cor_bg": "230,126,34,255",       # Terracota Laranja
        "border": "160,64,0,255",
        "icon": "./simbologia/maki/circle.svg",
        "size_bg": "6.5",
        "size_icon": "4.5"
    }
]

for ml in root.findall(".//maplayer"):
    lname = str(ml.find('layername').text if ml.find('layername') is not None else '')
    if 'vegeta' in lname.lower() or 'flora' in lname.lower() or 'rvores matrizes' in lname.lower():
        novo_nome = "Biodiversidade: Fauna, Flora e Recursos Naturais"
        ml.find('layername').text = novo_nome
        print(f"  • Atualizando camada para: {novo_nome}")

        # Substitui renderer por categorizedSymbol
        old_r = ml.find('renderer-v2')
        if old_r is not None:
            ml.remove(old_r)

        new_r = ET.SubElement(ml, 'renderer-v2', {
            'attr': 'grupo_macro',
            'enableorderby': '0',
            'forceraster': '0',
            'referencescale': '-1',
            'symbollevels': '0',
            'type': 'categorizedSymbol'
        })

        cats_elem = ET.SubElement(new_r, 'categories')
        syms_elem = ET.SubElement(new_r, 'symbols')

        for i, cat in enumerate(CATEGORIAS):
            sym_name = str(i)
            # Entrada de categoria
            ET.SubElement(cats_elem, 'category', {
                'render': 'true',
                'symbol': sym_name,
                'value': cat['valor'],
                'label': cat['label']
            })

            # Símbolo composto (Fundo Circular + Ícone SVG Temático)
            sym = ET.SubElement(syms_elem, 'symbol', {
                'alpha': '1',
                'clip_to_extent': '1',
                'force_rhr': '0',
                'frame_rate': '10',
                'is_animated': '0',
                'name': sym_name,
                'type': 'marker'
            })
            ET.SubElement(sym, 'data_defined_properties')

            # Camada 1: Círculo de fundo colorido
            l1 = ET.SubElement(sym, 'layer', {
                'class': 'SimpleMarker', 'enabled': '1', 'locked': '0', 'pass': '0',
                'id': f'{{bg_cat_{i}}}'
            })
            opts1 = {
                'angle': '0',
                'color': cat['cor_bg'],
                'name': 'circle',
                'size': cat['size_bg'],
                'size_unit': 'MM',
                'outline_color': cat['border'],
                'outline_style': 'solid',
                'outline_width': '0.6',
                'outline_width_unit': 'MM'
            }
            for k, v in opts1.items():
                ET.SubElement(l1, 'Option', {'name': k, 'type': 'QString', 'value': v})

            # Camada 2: Ícone SVG temático
            l2 = ET.SubElement(sym, 'layer', {
                'class': 'SvgMarker', 'enabled': '1', 'locked': '0', 'pass': '0',
                'id': f'{{svg_cat_{i}}}'
            })
            opts2 = {
                'name': cat['icon'],
                'color': '255,255,255,255',
                'outline_color': '0,0,0,255',
                'outline_width': '0.1',
                'size': cat['size_icon'],
                'size_unit': 'MM'
            }
            for k, v in opts2.items():
                ET.SubElement(l2, 'Option', {'name': k, 'type': 'QString', 'value': v})

# Atualiza também na árvore de camadas
for grp in root.findall(".//layer-tree-group"):
    for lay in grp.findall("layer-tree-layer"):
        if 'vegeta' in lay.attrib.get('name', '').lower() or 'flora' in lay.attrib.get('name', '').lower():
            lay.attrib['name'] = "Biodiversidade: Fauna, Flora e Recursos Naturais"

# Salva QGS e recompacta QGZ
qgs_atualizado = ET.tostring(root, encoding="utf-8", xml_declaration=True)

with zipfile.ZipFile(QGZ_PATH, 'w', compression=zipfile.ZIP_DEFLATED) as z_out:
    z_out.writestr("tabuleiro_do_embaubal_e_vitoria_souzel.qgs", qgs_atualizado)
    for n, data in outras_partes.items():
        z_out.writestr(n, data)

print(f"\n[SUCESSO COMPLETO] Camada categorizada com ícones específicos e projeto QGIS atualizado!")
