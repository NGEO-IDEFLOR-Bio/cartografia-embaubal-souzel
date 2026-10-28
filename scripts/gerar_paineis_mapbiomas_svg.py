# -*- coding: utf-8 -*-
"""
Gera os painéis gráficos SVG técnicos para Uso e Cobertura do Solo (MapBiomas Coleção 11)
baseados nos dados oficiais extraídos via Google Earth Engine (GEE).

Dimensões exatas:
Largura: 111.752 mm
Altura: 185.429 mm
Fonte: Segoe UI Variable Small Semibold
Estilo: Técnico, minimalista, retângulos retos (rx=0 ry=0), textos grandes e legíveis.
Sem título externo (já inserido no retângulo do layout QGIS).
"""

import pandas as pd
import os
import xml.sax.saxutils as saxutils

df = pd.read_csv("camadas/tabelas/estatisticas_mapbiomas_c11_revis_rds.csv")

# Tabela oficial de cores MapBiomas C11
CORES = {
    6:  {'nome': 'Floresta Alagável', 'hex': '#007785'},
    33: {'nome': 'Rio, Lago e Oceano', 'hex': '#2532e4'},
    11: {'nome': 'Campo Alagado e Área Pantanosa', 'hex': '#519799'},
    15: {'nome': 'Pastagem', 'hex': '#edde8e'},
    21: {'nome': 'Mosaico de Usos', 'hex': '#ffefc3'},
    3:  {'nome': 'Formação Florestal', 'hex': '#1f8d49'},
    12: {'nome': 'Formação Campestre', 'hex': '#d6bc74'},
    4:  {'nome': 'Formação Savânica', 'hex': '#7dc975'},
    25: {'nome': 'Outras Áreas não Vegetadas', 'hex': '#db4d4f'},
}

ANOS = [1985, 1995, 2005, 2015, 2024]
W = 111.752
H = 185.429

def gerar_painel_svg(sub_df, nome_unidade, subtitulo, output_path):
    nome_unidade_xml = saxutils.escape(nome_unidade)
    subtitulo_xml = saxutils.escape(subtitulo)
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">')
    svg.append(f'  <!-- Fundo transparente -->')
    svg.append(f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff" fill-opacity="0" />')

    # CABEÇALHO TÉCNICO INTERNO (Discreto e informativo)
    svg.append(f'  <!-- Cabeçalho Informativo -->')
    svg.append(f'  <text x="4.0" y="7.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.6" font-weight="bold" fill="#1b3626">{nome_unidade_xml}</text>')
    svg.append(f'  <text x="4.0" y="12.0" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.7" fill="#666666">{subtitulo_xml}</text>')
    svg.append(f'  <line x1="4.0" y1="14.5" x2="{W-4.0}" y2="14.5" stroke="#cccccc" stroke-width="0.4" />')

    # ÁREA DO GRÁFICO DE BARRAS EMPILHADAS (STACKED 100%)
    # Destaque visual grande: topo y=19, altura ~82mm
    chart_x = 15.0
    chart_y = 19.0
    chart_w = W - chart_x - 5.0  # ~91.7 mm
    chart_h = 80.0

    # Grid horizontal de porcentagem (0%, 25%, 50%, 75%, 100%)
    for pct in [0, 25, 50, 75, 100]:
        y_pos = chart_y + chart_h - (pct / 100.0 * chart_h)
        svg.append(f'  <line x1="{chart_x}" y1="{y_pos:.2f}" x2="{chart_x + chart_w}" y2="{y_pos:.2f}" stroke="#e2e2e2" stroke-width="0.35" stroke-dasharray="1.0,1.0" />')
        svg.append(f'  <text x="{chart_x - 1.8}" y="{y_pos + 1.0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" font-weight="bold" fill="#777777" text-anchor="end">{pct}%</text>')

    # Linha base do gráfico
    svg.append(f'  <line x1="{chart_x}" y1="{chart_y + chart_h}" x2="{chart_x + chart_w}" y2="{chart_y + chart_h}" stroke="#333333" stroke-width="0.6" />')

    # BARRAS EMPILHADAS LARGAS
    bar_w = 12.5
    gap = (chart_w - (len(ANOS) * bar_w)) / (len(ANOS) + 1)

    # Identificar classes presentes nesta UC
    classes_uc = sub_df.groupby('Classe_ID')['Percentual'].max()
    classes_relevantes = [cid for cid, pmax in classes_uc.items() if pmax >= 0.2]
    # Garantir ordem visual coerente: Rio na base, depois floresta, etc.
    ordem_padrao = [33, 6, 11, 15, 21, 3, 12, 4, 25]
    classes_ordenadas = [c for c in ordem_padrao if c in classes_relevantes]

    for i, ano in enumerate(ANOS):
        bx = chart_x + gap + i * (bar_w + gap)
        df_ano = sub_df[sub_df['Ano'] == ano]
        pct_map = dict(zip(df_ano['Classe_ID'], df_ano['Percentual']))

        acum_y = chart_y + chart_h
        for cid in classes_ordenadas:
            pct = pct_map.get(cid, 0.0)
            if pct <= 0.05:
                continue
            seg_h = (pct / 100.0) * chart_h
            top_y = acum_y - seg_h
            cor = CORES.get(cid, {}).get('hex', '#888888')

            svg.append(f'  <rect x="{bx:.2f}" y="{top_y:.2f}" width="{bar_w:.2f}" height="{seg_h:.2f}" fill="{cor}" stroke="#222222" stroke-width="0.2" rx="0" ry="0" />')

            # Rótulo em percentual se houver altura suficiente (>= 5mm)
            if seg_h >= 5.5 and pct >= 5.0:
                txt_color = "#ffffff" if cid in [33, 6, 3] else "#111111"
                svg.append(f'  <text x="{bx + bar_w/2:.2f}" y="{top_y + seg_h/2 + 1.0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" font-weight="bold" fill="{txt_color}" text-anchor="middle">{pct:.0f}%</text>')

            acum_y = top_y

        # Rótulo do Ano no rodapé de cada barra
        svg.append(f'  <text x="{bx + bar_w/2:.2f}" y="{chart_y + chart_h + 4.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.0" font-weight="bold" fill="#222222" text-anchor="middle">{ano}</text>')

    # DIVISÓRIA CENTRAL
    sec_y = chart_y + chart_h + 8.5
    svg.append(f'  <line x1="4.0" y1="{sec_y:.2f}" x2="{W-4.0}" y2="{sec_y:.2f}" stroke="#cccccc" stroke-width="0.4" />')

    # SEÇÃO INFERIOR: CARTÕES TÉCNICOS DE RESUMO DAS CLASSES PRINCIPAIS (2024 vs 1985)
    # Título da seção
    svg.append(f'  <text x="4.0" y="{sec_y + 4.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.9" font-weight="bold" fill="#1b3626">PANORAMA DAS CLASSES DE COBERTURA</text>')

    df_2024 = sub_df[sub_df['Ano'] == 2024].sort_values(by='Percentual', ascending=False)
    df_1985 = sub_df[sub_df['Ano'] == 1985]
    map_85_ha = dict(zip(df_1985['Classe_ID'], df_1985['Area_ha']))

    # Tabela clara e espaçosa
    tab_y = sec_y + 8.5
    # Cabeçalho da tabela
    svg.append(f'  <rect x="4.0" y="{tab_y:.2f}" width="{W - 8.0}" height="4.5" fill="#eef2ef" rx="0" ry="0" />')
    svg.append(f'  <text x="6.0" y="{tab_y + 3.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" font-weight="bold" fill="#333333">Classe</text>')
    svg.append(f'  <text x="{W - 35.0}" y="{tab_y + 3.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" font-weight="bold" fill="#333333" text-anchor="end">1985 (ha)</text>')
    svg.append(f'  <text x="{W - 17.0}" y="{tab_y + 3.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" font-weight="bold" fill="#333333" text-anchor="end">2024 (ha)</text>')
    svg.append(f'  <text x="{W - 5.5}" y="{tab_y + 3.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" font-weight="bold" fill="#1b3626" text-anchor="end">2024 %</text>')

    row_y = tab_y + 5.0
    # Pegar as classes principais (até 5 ou 6 para caber com perfeição)
    top_classes = [r for _, r in df_2024.iterrows() if r['Percentual'] >= 0.1][:6]

    for r in top_classes:
        cid = int(r['Classe_ID'])
        nome_cl = CORES.get(cid, {}).get('nome', r['Classe_Nome'])
        cor = CORES.get(cid, {}).get('hex', '#888888')
        ha_24 = r['Area_ha']
        pct_24 = r['Percentual']
        ha_85 = map_85_ha.get(cid, 0.0)

        # Fundo zebrado sutil opcional ou linha divisória
        svg.append(f'  <!-- Linha {nome_cl} -->')
        # Quadrado colorido
        svg.append(f'  <rect x="5.5" y="{row_y + 1.0:.2f}" width="3.0" height="3.0" fill="{cor}" stroke="#222222" stroke-width="0.2" rx="0" ry="0" />')
        # Nome da classe
        nome_curto = nome_cl if len(nome_cl) <= 20 else nome_cl[:18] + '...'
        svg.append(f'  <text x="9.8" y="{row_y + 3.3:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.3" fill="#222222">{nome_curto}</text>')
        # Valores numéricos
        svg.append(f'  <text x="{W - 35.0}" y="{row_y + 3.3:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.3" fill="#666666" text-anchor="end">{ha_85:,.0f}</text>')
        svg.append(f'  <text x="{W - 17.0}" y="{row_y + 3.3:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.3" font-weight="bold" fill="#222222" text-anchor="end">{ha_24:,.0f}</text>')
        svg.append(f'  <text x="{W - 5.5}" y="{row_y + 3.3:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" font-weight="bold" fill="#1b3626" text-anchor="end">{pct_24:.1f}%</text>')
        
        # Divisória
        svg.append(f'  <line x1="5.0" y1="{row_y + 5.0:.2f}" x2="{W - 5.0}" y2="{row_y + 5.0:.2f}" stroke="#e8e8e8" stroke-width="0.25" />')
        row_y += 5.2

    # RODAPÉ TÉCNICO
    nota_y = H - 6.5
    svg.append(f'  <line x1="4.0" y1="{nota_y - 2.5:.2f}" x2="{W-4.0}" y2="{nota_y - 2.5:.2f}" stroke="#cccccc" stroke-width="0.3" />')
    svg.append(f'  <text x="4.0" y="{nota_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.1" fill="#777777">Fonte: MapBiomas Brasil (Coleção 11). Processamento: GEE / IDEFLOR-Bio.</text>')
    svg.append(f'  <text x="4.0" y="{nota_y + 3.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.1" fill="#777777">Cálculo zonal geodésico sobre polígono oficial do Decreto de Criação.</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Gerado: {output_path}")


# 1. Gerar para REVIS Tabuleiro do Embaubal
df_revis = df[df['Categoria'] == 'REVIS']
gerar_painel_svg(
    df_revis,
    nome_unidade="REVIS TABULEIRO DO EMBAUBAL",
    subtitulo="Área Total: 4.035,7 ha | Série 1985 – 2024",
    output_path="paineis_tematicos_svg/grafico_mapbiomas_revis_embaubal.svg"
)

# 2. Gerar para RDS Vitória de Souzel
df_rds = df[df['Categoria'] == 'RDS']
gerar_painel_svg(
    df_rds,
    nome_unidade="RDS VITÓRIA DE SOUZEL",
    subtitulo="Área Total: 22.987,4 ha | Série 1985 – 2024",
    output_path="paineis_tematicos_svg/grafico_mapbiomas_rds_souzel.svg"
)

# 3. Gerar Consolidado (REVIS + RDS Juntas)
df_total = df.groupby(['Ano', 'Classe_ID', 'Classe_Nome'], as_index=False).agg({'Area_ha': 'sum'})
# Recalcular % total
area_total_ano = df_total.groupby('Ano')['Area_ha'].transform('sum')
df_total['Percentual'] = (df_total['Area_ha'] / area_total_ano) * 100.0

gerar_painel_svg(
    df_total,
    nome_unidade="REVIS TABULEIRO DO EMBAUBAL & RDS VITÓRIA DE SOUZEL",
    subtitulo="Área Total Consolidada: 27.023,1 ha | 1985 – 2024",
    output_path="paineis_tematicos_svg/grafico_mapbiomas_consolidado_ambas_ucs.svg"
)
