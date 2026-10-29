# -*- coding: utf-8 -*-
"""
Script de Limpeza Cartográfica, Deduplicação e Atualização da Simbologia QGIS
Projeto: REVIS Tabuleiro do Embaubal e RDS Vitória de Souzel

Executa:
1. Backup de segurança de todas as camadas vetoriais em camadas/backup_pre_limpeza/
2. Remoção de pontos de tracklog/atividade que não são acessos reais ('quarta-feira', 'almoço', etc.)
3. Deduplicação inteligente de pontos com passadas múltiplas (distância <= 25m preservando o nome mais completo)
4. Aumento da simbologia de Quelônios (de 5.5mm/6.7mm para 8.5mm/10.0mm)
5. Criação de marcador institucional de alto destaque para a 'BASE DO IDEFLOR-BIO' (emblema verde floresta e dourado com ícone de posto de fiscalização)
6. Atualização do arquivo QGIS (tabuleiro_do_embaubal_e_vitoria_souzel.qgz) e do consolidado de pontos
"""

import os
import glob
import shutil
import zipfile
import difflib
import xml.etree.ElementTree as ET
import numpy as np
import geopandas as gpd
import pandas as pd
from scipy.spatial import cKDTree

DIR_CAMADAS = "camadas"
DIR_BACKUP = "camadas/backup_pre_limpeza"
QGZ_PATH = "tabuleiro_do_embaubal_e_vitoria_souzel.qgz"

os.makedirs(DIR_BACKUP, exist_ok=True)

# -------------------------------------------------------------------------
# ETAPA 1: BACKUP DAS CAMADAS ORIGINAIS
# -------------------------------------------------------------------------
print("--- [1/5] Realizando backup de segurança das camadas ---")
for f in glob.glob(f"{DIR_CAMADAS}/*.geojson"):
    shutil.copy2(f, os.path.join(DIR_BACKUP, os.path.basename(f)))
print(f"[OK] Backup salvo em: {DIR_BACKUP}/")

# -------------------------------------------------------------------------
# ETAPA 2: FUNÇÕES DE LIMPEZA E DEDUPLICAÇÃO
# -------------------------------------------------------------------------
def eh_ponto_tracklog_invalido(nome, subcategoria=""):
    txt = f"{nome} {subcategoria}".lower()
    dias = ['segunda', 'terça', 'terca', 'quarta', 'quinta', 'sexta', 'sábado', 'sabado', 'domingo']
    atividades = ['morning', 'afternoon', 'evening', 'almoço', 'almoco', 'off-road', 'caminhando', 'corrida', 'activity']
    
    tem_dia = any(d in txt for d in dias)
    tem_ativ = any(a in txt for a in atividades)
    return tem_dia or tem_ativ

def score_qualidade_nome(nome):
    s = str(nome or '').strip()
    if not s: return -10
    sl = s.lower()
    if sl in ['desconhecido', 'abandonado', 'rancho desconhecido', 'sem nome', 'apoio de pesca desconhecido']: return 0
    if sl.isdigit(): return 1
    return 10 + len(s) + (s.count(' ') * 6)

def deduplicar_camada_pontos(gdf, nome_camada, dist_limite=25.0):
    if len(gdf) <= 1:
        if not isinstance(gdf, gpd.GeoDataFrame):
            gdf = gpd.GeoDataFrame(gdf, geometry='geometry', crs=gdf.crs if hasattr(gdf, 'crs') else "EPSG:4674")
        return gdf, 0

    gdf_utm = gdf.to_crs(epsg=31982)
    coords = np.array([(p.x, p.y) for p in gdf_utm.geometry])
    tree = cKDTree(coords)
    pairs = tree.query_pairs(r=dist_limite)

    removidos = set()
    detalhes = []

    for i, j in pairs:
        if i in removidos or j in removidos:
            continue
        p1 = gdf.iloc[i]
        p2 = gdf.iloc[j]
        d = np.linalg.norm(coords[i] - coords[j])
        n1 = str(p1.get('nome', '') or '').strip()
        n2 = str(p2.get('nome', '') or '').strip()

        sim = difflib.SequenceMatcher(None, n1.lower(), n2.lower()).ratio()

        eh_dup = False
        if d <= 5.0:
            eh_dup = True
        elif d <= dist_limite:
            if sim > 0.40 or (n1.lower() in n2.lower()) or (n2.lower() in n1.lower()):
                eh_dup = True
            elif any(k in n1.lower() for k in ['desconhecido', 'rancho', 'pesca']) and any(k in n2.lower() for k in ['desconhecido', 'rancho', 'pesca']):
                eh_dup = True

        if eh_dup:
            sc1 = score_qualidade_nome(n1)
            sc2 = score_qualidade_nome(n2)
            if sc1 >= sc2:
                manter, tirar = i, j
                m_nome, r_nome = n1, n2
                m_id, r_id = p1.get('id'), p2.get('id')
            else:
                manter, tirar = j, i
                m_nome, r_nome = n2, n1
                m_id, r_id = p2.get('id'), p1.get('id')

            removidos.add(tirar)
            detalhes.append((d, m_id, m_nome, r_id, r_nome))

    df_drop = gdf.drop(index=list(removidos)).reset_index(drop=True)
    gdf_limpo = gpd.GeoDataFrame(df_drop, geometry='geometry', crs=gdf.crs)
    return gdf_limpo, len(removidos)

# -------------------------------------------------------------------------
# ETAPA 3: PROCESSAMENTO DAS CAMADAS VETORIAIS
# -------------------------------------------------------------------------
print("\n--- [2/5] Limpando tracklogs e deduplicando pontos próximos ---")

camadas_para_processar = [
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

total_removidos_geral = 0

for c_name in camadas_para_processar:
    fpath = os.path.join(DIR_CAMADAS, c_name)
    if not os.path.exists(fpath): continue
    
    gdf = gpd.read_file(fpath)
    ini_count = len(gdf)

    # 1. Filtra tracklogs falsos ('quarta-feira', 'almoço', etc.)
    mask_invalido = gdf.apply(lambda r: eh_ponto_tracklog_invalido(r.get('nome', ''), r.get('subcategoria', '')), axis=1)
    qtd_track = int(mask_invalido.sum())
    
    gdf_filtrado = gdf[~mask_invalido].copy()

    # 2. Deduplica pontos por proximidade geográfica
    if len(gdf_filtrado) > 0:
        gdf_limpo, qtd_dup = deduplicar_camada_pontos(gdf_filtrado, c_name, dist_limite=25.0)
    else:
        gdf_limpo = gdf_filtrado
        qtd_dup = 0

    # Salva camada limpa
    gdf_limpo.to_file(fpath, driver="GeoJSON", encoding="utf-8")
    
    rem_nesta = ini_count - len(gdf_limpo)
    total_removidos_geral += rem_nesta
    print(f"  • {c_name}: {ini_count} -> {len(gdf_limpo)} pontos (Removidos: {qtd_track} tracklogs falsos + {qtd_dup} duplicatas)")

# -------------------------------------------------------------------------
# ETAPA 4: RECONSOLIDAÇÃO DA CAMADA GERAL DE PONTOS
# -------------------------------------------------------------------------
print("\n--- [3/5] Reconsolidando camada geral de pontos de campo ---")
gdfs_validos = []
for c_name in camadas_para_processar:
    p = os.path.join(DIR_CAMADAS, c_name)
    if os.path.exists(p):
        g = gpd.read_file(p)
        if len(g) > 0:
            gdfs_validos.append(g.to_crs(epsg=4674))

if gdfs_validos:
    gdf_cons = pd.concat(gdfs_validos, ignore_index=True)
    gdf_cons = gpd.GeoDataFrame(gdf_cons, geometry='geometry', crs="EPSG:4674")
    
    gdf_cons.to_file(f"{DIR_CAMADAS}/pontos_revis_rds_consolidado.geojson", driver="GeoJSON", encoding="utf-8")
    gdf_cons.to_file(f"{DIR_CAMADAS}/pontos_revis_rds_consolidado.gpkg", layer="pontos_campo", driver="GPKG")
    print(f"[OK] Consolidado atualizado com {len(gdf_cons)} pontos limpos e únicos.")

# -------------------------------------------------------------------------
# ETAPA 5: ATUALIZAÇÃO DA SIMBOLOGIA NO PROJETO QGIS (.QGZ)
# -------------------------------------------------------------------------
print("\n--- [4/5] Atualizando simbologia no QGIS: Quelônios maiores e Base IDEFLOR destacada ---")

with zipfile.ZipFile(QGZ_PATH, 'r') as z:
    qgs_bytes = z.read("tabuleiro_do_embaubal_e_vitoria_souzel.qgs")
    outras_partes = {n: z.read(n) for n in z.namelist() if n != "tabuleiro_do_embaubal_e_vitoria_souzel.qgs"}

root = ET.fromstring(qgs_bytes)

# 1. Aumento da simbologia de Quelônios
for ml in root.findall(".//maplayer"):
    lname = str(ml.find('layername').text if ml.find('layername') is not None else '')
    if any(k in lname.lower() for k in ['desova', 'quelônios', 'quelonios']):
        print(f"  • Aumentando tamanho dos ícones de Quelônios na camada: {lname}")
        renderer = ml.find('renderer-v2')
        if renderer is not None:
            # SimpleMarker (fundo circular verde/amarelo): aumenta para 10.0mm
            for opt in renderer.findall(".//layer[@class='SimpleMarker']//Option"):
                if opt.attrib.get('name') == 'size':
                    opt.attrib['value'] = "10.0"
                elif opt.attrib.get('name') == 'outline_width':
                    opt.attrib['value'] = "1.0"
            # SvgMarker (ícone da tartaruga): aumenta para 8.5mm
            for opt in renderer.findall(".//layer[@class='SvgMarker']//Option"):
                if opt.attrib.get('name') == 'size':
                    opt.attrib['value'] = "8.5"

# 2. Marcador diferenciado de alto destaque para a BASE DO IDEFLOR-BIO
for ml in root.findall(".//maplayer"):
    lid = str(ml.find('id').text if ml.find('id') is not None else '')
    lname = str(ml.find('layername').text if ml.find('layername') is not None else '')
    if 'base_ideflor' in lid.lower() or 'base do ideflor' in lname.lower():
        print(f"  • Configurando marcador de honra/destaque para: {lname}")
        renderer = ml.find('renderer-v2')
        if renderer is not None:
            symbols = renderer.find('symbols')
            if symbols is not None and len(symbols) > 0:
                sym = symbols[0]
                # Remove camadas de símbolos simples anteriores
                for old_l in list(sym.findall('layer')):
                    sym.remove(old_l)

                # Camada 1: Círculo de fundo verde floresta institucional
                l1 = ET.SubElement(sym, 'layer', {
                    'class': 'SimpleMarker',
                    'enabled': '1',
                    'locked': '0',
                    'pass': '0',
                    'id': '{base_ideflor_bg}'
                })
                opts1 = {
                    'angle': '0',
                    'color': '14,77,42,255',            # Verde Floresta Oficial IDEFLOR
                    'name': 'circle',
                    'size': '11.0',                     # Tamanho proeminente
                    'size_unit': 'MM',
                    'outline_color': '241,196,15,255',  # Borda Dourada Elegante
                    'outline_style': 'solid',
                    'outline_width': '1.2',
                    'outline_width_unit': 'MM'
                }
                for k, v in opts1.items():
                    ET.SubElement(l1, 'Option', {'name': k, 'type': 'QString', 'value': v})

                # Camada 2: Anel interno branco de acabamento cartográfico
                l2 = ET.SubElement(sym, 'layer', {
                    'class': 'SimpleMarker',
                    'enabled': '1',
                    'locked': '0',
                    'pass': '0',
                    'id': '{base_ideflor_ring}'
                })
                opts2 = {
                    'angle': '0',
                    'color': '0,0,0,0',                 # Transparente
                    'name': 'circle',
                    'size': '8.8',
                    'size_unit': 'MM',
                    'outline_color': '255,255,255,220', # Anel branco fino
                    'outline_style': 'solid',
                    'outline_width': '0.4',
                    'outline_width_unit': 'MM'
                }
                for k, v in opts2.items():
                    ET.SubElement(l2, 'Option', {'name': k, 'type': 'QString', 'value': v})

                # Camada 3: Ícone SVG Maki 'Ranger Station' em branco
                l3 = ET.SubElement(sym, 'layer', {
                    'class': 'SvgMarker',
                    'enabled': '1',
                    'locked': '0',
                    'pass': '0',
                    'id': '{base_ideflor_icon}'
                })
                opts3 = {
                    'name': './simbologia/maki/ranger-station.svg',
                    'color': '255,255,255,255',         # Branco puro
                    'outline_color': '14,77,42,255',
                    'outline_width': '0.1',
                    'size': '6.8',
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

print(f"\n[SUCESSO] QGZ atualizado com sucesso!")
print(f"Total de pontos duplicados ou espúrios eliminados: {total_removidos_geral}")
