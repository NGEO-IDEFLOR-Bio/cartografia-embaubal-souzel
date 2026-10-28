# -*- coding: utf-8 -*-
"""
Gerador de Produtos Cartográficos e Acadêmicos - MapBiomas Coleção 11
1. 5 Painéis Anuais (1985, 1995, 2005, 2015, 2024) para o Layout QGIS (111.752 x 185.429 mm)
2. Gráfico Geral da Série Histórica para Relatório Acadêmico (170 x 110 mm)
3. Diagrama de Sankey de Transições 1985-2024 para Relatório Acadêmico (180 x 115 mm)
"""

import pandas as pd
import json
import os
import xml.sax.saxutils as saxutils

# 1. Carregar dados consolidados
df = pd.read_csv("camadas/tabelas/estatisticas_mapbiomas_c11_revis_rds.csv")

# Agrupar consolidadas (REVIS + RDS juntos)
df_tot = df.groupby(['Ano', 'Classe_ID', 'Classe_Nome'], as_index=False)['Area_ha'].sum()
tot_ano = df_tot.groupby('Ano')['Area_ha'].transform('sum')
df_tot['Percentual'] = (df_tot['Area_ha'] / tot_ano) * 100.0

# Cores oficiais da Coleção 11
CORES = {
    6:  {'nome': 'Floresta Alagável', 'hex': '#007785', 'borda': '#005560'},
    33: {'nome': 'Rio, Lago e Oceano', 'hex': '#2532e4', 'borda': '#1824b0'},
    11: {'nome': 'Campo Alagado / Pantanoso', 'hex': '#519799', 'borda': '#3e7678'},
    15: {'nome': 'Pastagem', 'hex': '#edde8e', 'borda': '#c5b66c'},
    21: {'nome': 'Mosaico de Usos', 'hex': '#ffefc3', 'borda': '#d9caa0'},
    3:  {'nome': 'Formação Florestal', 'hex': '#1f8d49', 'borda': '#146031'},
    12: {'nome': 'Formação Campestre', 'hex': '#d6bc74', 'borda': '#b29c5e'},
    4:  {'nome': 'Formação Savânica', 'hex': '#7dc975', 'borda': '#5aa852'},
    25: {'nome': 'Outras Áreas não Veg.', 'hex': '#db4d4f', 'borda': '#a62e30'},
}

os.makedirs("paineis_tematicos_svg", exist_ok=True)

# ==============================================================================
# FUNÇÃO 1: PAINÉIS ANUAIS PARA O MAPA (111.752 x 185.429 mm)
# ==============================================================================
def gerar_painel_anual(ano, output_path):
    W = 111.752
    H = 185.429
    
    sub = df_tot[df_tot['Ano'] == ano].sort_values(by='Area_ha', ascending=False)
    area_tot = sub['Area_ha'].sum()
    
    # Classes principais (>= 0.1% ou top 5)
    classes_mostradas = [r for _, r in sub.iterrows() if r['Percentual'] >= 0.1][:5]
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">')
    svg.append(f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff" fill-opacity="0" />')

    # 1. BLOCO DE DESTAQUE DO ANO (Grande e imponente)
    svg.append(f'  <!-- Card Destaque Ano -->')
    svg.append(f'  <rect x="4.0" y="4.0" width="{W-8.0}" height="24.0" fill="#f4f7f5" stroke="#1b3626" stroke-width="0.8" rx="0" ry="0" />')
    svg.append(f'  <text x="8.0" y="14.0" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.2" fill="#555555">ANO DE REFERÊNCIA</text>')
    svg.append(f'  <text x="8.0" y="24.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="9.5" font-weight="bold" fill="#1b3626">{ano}</text>')
    
    # Área total da UC no canto direito do card
    svg.append(f'  <text x="{W-8.0}" y="14.0" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" fill="#777777" text-anchor="end">ÁREA MAPEADA</text>')
    svg.append(f'  <text x="{W-8.0}" y="23.0" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="5.2" font-weight="bold" fill="#222222" text-anchor="end">{area_tot:,.0f} ha</text>')

    # 2. TÍTULO DA SEÇÃO DE BARRAS
    bar_section_y = 34.0
    svg.append(f'  <text x="4.0" y="{bar_section_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.6" font-weight="bold" fill="#1b3626">DISTRIBUIÇÃO DA COBERTURA</text>')
    svg.append(f'  <line x1="4.0" y1="{bar_section_y + 2.5:.2f}" x2="{W-4.0}" y2="{bar_section_y + 2.5:.2f}" stroke="#cccccc" stroke-width="0.5" />')

    # 3. GRÁFICOS DE BARRAS HORIZONTAIS LARGAS
    cur_y = bar_section_y + 7.5
    bar_max_w = W - 38.0  # espaço até o número de porcentagem
    
    for r in classes_mostradas:
        cid = int(r['Classe_ID'])
        nome = CORES.get(cid, {}).get('nome', r['Classe_Nome'])
        cor = CORES.get(cid, {}).get('hex', '#888888')
        ha = r['Area_ha']
        pct = r['Percentual']

        # Nome da classe e área em ha
        svg.append(f'  <text x="4.0" y="{cur_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.1" font-weight="bold" fill="#222222">{nome}</text>')
        svg.append(f'  <text x="{W-4.0}" y="{cur_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.0" font-weight="bold" fill="#1b3626" text-anchor="end">{pct:.1f}%</text>')

        # Barra de fundo cinza
        bar_y = cur_y + 1.8
        svg.append(f'  <rect x="4.0" y="{bar_y:.2f}" width="{bar_max_w:.2f}" height="4.8" fill="#e9ecea" rx="0" ry="0" />')
        
        # Barra de preenchimento proporcional (100% = bar_max_w)
        fill_w = max(1.5, (pct / 100.0) * bar_max_w)
        svg.append(f'  <rect x="4.0" y="{bar_y:.2f}" width="{fill_w:.2f}" height="4.8" fill="{cor}" stroke="#222222" stroke-width="0.25" rx="0" ry="0" />')
        
        # Hectares logo ao lado da barra
        svg.append(f'  <text x="{W-4.0}" y="{bar_y + 3.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" fill="#666666" text-anchor="end">{ha:,.0f} ha</text>')

        cur_y += 12.0

    # 4. TABELA RESUMO DETALHADA NO BLOCO INFERIOR
    tab_y = cur_y + 4.0
    svg.append(f'  <line x1="4.0" y1="{tab_y:.2f}" x2="{W-4.0}" y2="{tab_y:.2f}" stroke="#cccccc" stroke-width="0.5" />')
    svg.append(f'  <text x="4.0" y="{tab_y + 5.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.4" font-weight="bold" fill="#1b3626">QUADRO QUANTITATIVO ({ano})</text>')
    
    # Cabeçalho da tabela
    head_y = tab_y + 8.5
    svg.append(f'  <rect x="4.0" y="{head_y:.2f}" width="{W-8.0}" height="5.5" fill="#e6ede8" rx="0" ry="0" />')
    svg.append(f'  <text x="6.0" y="{head_y + 3.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" font-weight="bold" fill="#222222">Classe</text>')
    svg.append(f'  <text x="{W-24.0}" y="{head_y + 3.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" font-weight="bold" fill="#222222" text-anchor="end">Área (ha)</text>')
    svg.append(f'  <text x="{W-6.0}" y="{head_y + 3.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" font-weight="bold" fill="#1b3626" text-anchor="end">Proporção</text>')

    r_y = head_y + 5.5
    for r in classes_mostradas:
        cid = int(r['Classe_ID'])
        nome = CORES.get(cid, {}).get('nome', r['Classe_Nome'])
        cor = CORES.get(cid, {}).get('hex', '#888888')
        ha = r['Area_ha']
        pct = r['Percentual']

        # Linha
        svg.append(f'  <rect x="5.5" y="{r_y + 1.2:.2f}" width="3.2" height="3.2" fill="{cor}" stroke="#222222" stroke-width="0.25" rx="0" ry="0" />')
        nome_disp = nome if len(nome) <= 22 else nome[:20] + '..'
        svg.append(f'  <text x="10.5" y="{r_y + 3.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" fill="#222222">{nome_disp}</text>')
        svg.append(f'  <text x="{W-24.0}" y="{r_y + 3.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" font-weight="bold" fill="#333333" text-anchor="end">{ha:,.0f} ha</text>')
        svg.append(f'  <text x="{W-6.0}" y="{r_y + 3.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.7" font-weight="bold" fill="#1b3626" text-anchor="end">{pct:.1f}%</text>')
        svg.append(f'  <line x1="4.0" y1="{r_y + 5.5:.2f}" x2="{W-4.0}" y2="{r_y + 5.5:.2f}" stroke="#eeeeee" stroke-width="0.3" />')
        r_y += 5.8

    # Linha Total
    svg.append(f'  <rect x="4.0" y="{r_y + 1.0:.2f}" width="{W-8.0}" height="6.0" fill="#f4f7f5" rx="0" ry="0" />')
    svg.append(f'  <text x="6.0" y="{r_y + 5.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.8" font-weight="bold" fill="#1b3626">TOTAL</text>')
    svg.append(f'  <text x="{W-24.0}" y="{r_y + 5.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.8" font-weight="bold" fill="#1b3626" text-anchor="end">{area_tot:,.0f} ha</text>')
    svg.append(f'  <text x="{W-6.0}" y="{r_y + 5.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.8" font-weight="bold" fill="#1b3626" text-anchor="end">100,0%</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Painel Anual gerado: {output_path}")

for ano in [1985, 1995, 2005, 2015, 2024]:
    gerar_painel_anual(ano, f"paineis_tematicos_svg/painel_mapa_ano_{ano}.svg")


# ==============================================================================
# FUNÇÃO 2: GRÁFICO GERAL DA SÉRIE HISTÓRICA PARA RELATÓRIO ACADÊMICO (170 x 110 mm)
# ==============================================================================
def gerar_grafico_relatorio_academico(output_path):
    W = 170.0
    H = 110.0
    
    anos = [1985, 1995, 2005, 2015, 2024]
    classes_relev = [6, 33, 11, 15, 21]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">')
    svg.append(f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff" stroke="#dddddd" stroke-width="0.4" rx="0" ry="0" />')

    # Título Acadêmico da Figura
    svg.append(f'  <text x="8.0" y="9.0" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.8" font-weight="bold" fill="#1b3626">Evolução Temporal do Uso e Cobertura da Terra (1985 – 2024)</text>')
    svg.append(f'  <text x="8.0" y="13.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" fill="#666666">REVIS Tabuleiro do Embaubal e RDS Vitória de Souzel (Área Consolidada: 27.023 ha)</text>')
    svg.append(f'  <line x1="8.0" y1="16.0" x2="{W-8.0}" y2="16.0" stroke="#cccccc" stroke-width="0.4" />')

    # Área do Gráfico
    cx = 20.0
    cy = 22.0
    cw = 100.0
    ch = 68.0

    # Grid Y (0 a 100%)
    for pct in [0, 20, 40, 60, 80, 100]:
        y_p = cy + ch - (pct / 100.0 * ch)
        svg.append(f'  <line x1="{cx}" y1="{y_p:.2f}" x2="{cx + cw}" y2="{y_p:.2f}" stroke="#e5e5e5" stroke-width="0.3" stroke-dasharray="1.0,1.0" />')
        svg.append(f'  <text x="{cx - 2.0}" y="{y_p + 1.0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" fill="#666666" text-anchor="end">{pct}%</text>')

    svg.append(f'  <line x1="{cx}" y1="{cy + ch}" x2="{cx + cw}" y2="{cy + ch}" stroke="#333333" stroke-width="0.6" />')

    # Barras empilhadas por ano
    bw = 13.0
    gap = (cw - len(anos)*bw) / (len(anos) + 1)

    for i, a in enumerate(anos):
        bx = cx + gap + i * (bw + gap)
        sub_a = df_tot[df_tot['Ano'] == a]
        pct_map = dict(zip(sub_a['Classe_ID'], sub_a['Percentual']))

        acum_y = cy + ch
        for cid in [33, 6, 11, 15, 21]:
            pct = pct_map.get(cid, 0.0)
            if pct <= 0.05: continue
            sh = (pct / 100.0) * ch
            ty = acum_y - sh
            cor = CORES[cid]['hex']
            svg.append(f'  <rect x="{bx:.2f}" y="{ty:.2f}" width="{bw:.2f}" height="{sh:.2f}" fill="{cor}" stroke="#222222" stroke-width="0.25" rx="0" ry="0" />')
            if sh >= 5.5 and pct >= 5.0:
                tc = "#ffffff" if cid in [33, 6] else "#111111"
                svg.append(f'  <text x="{bx + bw/2:.2f}" y="{ty + sh/2 + 0.9:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.5" font-weight="bold" fill="{tc}" text-anchor="middle">{pct:.0f}%</text>')
            acum_y = ty

        svg.append(f'  <text x="{bx + bw/2:.2f}" y="{cy + ch + 4.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.9" font-weight="bold" fill="#222222" text-anchor="middle">{a}</text>')

    # Legenda Lateral Direita
    lx = cx + cw + 7.0
    ly = cy + 4.0
    svg.append(f'  <text x="{lx}" y="{ly:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.8" font-weight="bold" fill="#1b3626">LEGENDA</text>')
    
    ly += 5.0
    for cid in [6, 33, 11, 15, 21]:
        cor = CORES[cid]['hex']
        nome = CORES[cid]['nome']
        # Quadrinho
        svg.append(f'  <rect x="{lx}" y="{ly:.2f}" width="4.0" height="4.0" fill="{cor}" stroke="#222222" stroke-width="0.25" rx="0" ry="0" />')
        svg.append(f'  <text x="{lx + 5.5}" y="{ly + 3.1:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.3" fill="#333333">{nome}</text>')
        # Valores 2024
        p24 = df_tot[(df_tot['Ano'] == 2024) & (df_tot['Classe_ID'] == cid)]['Percentual'].values[0]
        h24 = df_tot[(df_tot['Ano'] == 2024) & (df_tot['Classe_ID'] == cid)]['Area_ha'].values[0]
        svg.append(f'  <text x="{lx + 5.5}" y="{ly + 6.3:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.0" fill="#666666">2024: {h24:,.0f} ha ({p24:.1f}%)</text>')
        ly += 9.5

    # Rodapé Técnico do Gráfico
    svg.append(f'  <line x1="8.0" y1="{H-8.0}" x2="{W-8.0}" y2="{H-8.0}" stroke="#cccccc" stroke-width="0.3" />')
    svg.append(f'  <text x="8.0" y="{H-4.5}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.1" fill="#777777">Fonte: MapBiomas Brasil (Coleção 11, 30m). Processamento: IDEFLOR-Bio / DGMUC.</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Gráfico Geral de Relatório gerado: {output_path}")

gerar_grafico_relatorio_academico("paineis_tematicos_svg/relatorio_grafico_serie_historica.svg")


# ==============================================================================
# FUNÇÃO 3: DIAGRAMA DE SANKEY (1985 -> 2024) PARA RELATÓRIO ACADÊMICO (180 x 115 mm)
# ==============================================================================
def gerar_diagrama_sankey_academico(output_path):
    W = 180.0
    H = 115.0

    with open("camadas/tabelas/transicoes_mapbiomas_1985_2024.json", encoding="utf-8") as f:
        trans = json.load(f)

    # Filtrar apenas transições expressivas (>= 40 ha) para diagrama limpo e elegante
    trans_sig = [t for t in trans if t['ha'] >= 40.0]

    tot_ha = 27023.12

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">')
    svg.append(f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff" stroke="#dddddd" stroke-width="0.4" rx="0" ry="0" />')

    # Título Acadêmico
    svg.append(f'  <text x="8.0" y="8.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.8" font-weight="bold" fill="#1b3626">Diagrama de Transições da Cobertura da Terra (Sankey 1985 → 2024)</text>')
    svg.append(f'  <text x="8.0" y="12.8" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.5" fill="#666666">Dinâmica de estabilidade, erosão fluvial e antropização nas UCs Tabuleiro do Embaubal e Souzel</text>')
    svg.append(f'  <line x1="8.0" y1="15.0" x2="{W-8.0}" y2="15.0" stroke="#cccccc" stroke-width="0.4" />')

    # Coordenadas dos Nós (Esquerda = 1985, Direita = 2024)
    x_left = 32.0
    x_right = W - 35.0
    node_w = 7.0
    top_y = 24.0
    bottom_y = H - 12.0
    avail_h = bottom_y - top_y

    # Nós de 1985 (Origem)
    nodes_85 = [
        {'id': 6,  'nome': 'Floresta Alagável', 'ha': 13643.8, 'pct': 50.5},
        {'id': 33, 'nome': 'Rio/Lago (Água)',   'ha': 10039.2, 'pct': 37.1},
        {'id': 11, 'nome': 'Campo Alagado',    'ha': 3016.9,  'pct': 11.2},
        {'id': 21, 'nome': 'Mosaico de Usos',  'ha': 301.9,   'pct': 1.1},
    ]

    # Nós de 2024 (Destino)
    nodes_24 = [
        {'id': 6,  'nome': 'Floresta Alagável', 'ha': 11845.4, 'pct': 43.8},
        {'id': 33, 'nome': 'Rio/Lago (Água)',   'ha': 11500.3, 'pct': 42.6},
        {'id': 11, 'nome': 'Campo Alagado',    'ha': 2595.4,  'pct': 9.6},
        {'id': 15, 'nome': 'Pastagem',          'ha': 826.9,   'pct': 3.1},
        {'id': 21, 'nome': 'Mosaico de Usos',  'ha': 181.2,   'pct': 0.7},
    ]

    # Calcular posições Y e alturas proporcionais dos nós de 1985
    spacing_85 = 3.5
    total_gap_85 = spacing_85 * (len(nodes_85) - 1)
    scale_85 = (avail_h - total_gap_85) / tot_ha

    pos_y_85 = top_y
    for n in nodes_85:
        n_h = n['ha'] * scale_85
        n['y0'] = pos_y_85
        n['y1'] = pos_y_85 + n_h
        n['h'] = n_h
        n['cur_y'] = pos_y_85  # ponteiro para desenhar fluxos saindo
        pos_y_85 += n_h + spacing_85

    # Calcular posições Y e alturas proporcionais dos nós de 2024
    spacing_24 = 3.5
    total_gap_24 = spacing_24 * (len(nodes_24) - 1)
    scale_24 = (avail_h - total_gap_24) / tot_ha

    pos_y_24 = top_y
    for n in nodes_24:
        n_h = n['ha'] * scale_24
        n['y0'] = pos_y_24
        n['y1'] = pos_y_24 + n_h
        n['h'] = n_h
        n['cur_y'] = pos_y_24  # ponteiro para desenhar fluxos entrando
        pos_y_24 += n_h + spacing_24

    node_map_85 = {n['id']: n for n in nodes_85}
    node_map_24 = {n['id']: n for n in nodes_24}

    # DESENHAR FITAS DE FLUXO (RIBBONS) COM CURVAS BÉZIER CÚBICAS
    # Ordenar transições: maiores primeiro para visual elegante
    for t in trans_sig:
        src_id = t['from']
        dst_id = t['to']
        ha = t['ha']

        if src_id not in node_map_85 or dst_id not in node_map_24:
            continue

        n_src = node_map_85[src_id]
        n_dst = node_map_24[dst_id]

        flow_h_src = ha * scale_85
        flow_h_dst = ha * scale_24

        y0_src = n_src['cur_y']
        y1_src = y0_src + flow_h_src
        n_src['cur_y'] = y1_src

        y0_dst = n_dst['cur_y']
        y1_dst = y0_dst + flow_h_dst
        n_dst['cur_y'] = y1_dst

        # Cor do fluxo baseado na classe de origem
        cor_fluxo = CORES.get(src_id, {}).get('hex', '#888888')

        # Pontos de controle para Bézier suave
        x0 = x_left + node_w
        x1 = x_right
        dx = (x1 - x0) * 0.45

        # Path cúbico SVG
        d = (
            f"M {x0:.2f} {y0_src:.2f} "
            f"C {x0 + dx:.2f} {y0_src:.2f}, {x1 - dx:.2f} {y0_dst:.2f}, {x1:.2f} {y0_dst:.2f} "
            f"L {x1:.2f} {y1_dst:.2f} "
            f"C {x1 - dx:.2f} {y1_dst:.2f}, {x0 + dx:.2f} {y1_src:.2f}, {x0:.2f} {y1_src:.2f} Z"
        )

        svg.append(f'  <path d="{d}" fill="{cor_fluxo}" fill-opacity="0.48" stroke="{cor_fluxo}" stroke-width="0.15" />')

    # DESENHAR RETÂNGULOS DOS NÓS DE 1985 (ESQUERDA)
    svg.append(f'  <!-- Nós 1985 -->')
    svg.append(f'  <text x="{x_left + node_w/2:.2f}" y="{top_y - 3.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.2" font-weight="bold" fill="#1b3626" text-anchor="middle">ANO 1985</text>')
    
    for n in nodes_85:
        cor = CORES.get(n['id'], {}).get('hex', '#888888')
        svg.append(f'  <rect x="{x_left:.2f}" y="{n["y0"]:.2f}" width="{node_w:.2f}" height="{n["h"]:.2f}" fill="{cor}" stroke="#222222" stroke-width="0.3" rx="0" ry="0" />')
        # Rótulo à esquerda do nó
        svg.append(f'  <text x="{x_left - 2.5:.2f}" y="{n["y0"] + n["h"]/2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" font-weight="bold" fill="#222222" text-anchor="end">{n["nome"]}</text>')
        svg.append(f'  <text x="{x_left - 2.5:.2f}" y="{n["y0"] + n["h"]/2 + 3.0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.0" fill="#666666" text-anchor="end">{n["ha"]:,.0f} ha ({n["pct"]:.1f}%)</text>')

    # DESENHAR RETÂNGULOS DOS NÓS DE 2024 (DIREITA)
    svg.append(f'  <!-- Nós 2024 -->')
    svg.append(f'  <text x="{x_right + node_w/2:.2f}" y="{top_y - 3.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.2" font-weight="bold" fill="#1b3626" text-anchor="middle">ANO 2024</text>')

    for n in nodes_24:
        cor = CORES.get(n['id'], {}).get('hex', '#888888')
        svg.append(f'  <rect x="{x_right:.2f}" y="{n["y0"]:.2f}" width="{node_w:.2f}" height="{n["h"]:.2f}" fill="{cor}" stroke="#222222" stroke-width="0.3" rx="0" ry="0" />')
        # Rótulo à direita do nó
        svg.append(f'  <text x="{x_right + node_w + 2.5:.2f}" y="{n["y0"] + n["h"]/2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" font-weight="bold" fill="#222222">{n["nome"]}</text>')
        svg.append(f'  <text x="{x_right + node_w + 2.5:.2f}" y="{n["y0"] + n["h"]/2 + 3.0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.0" fill="#666666">{n["ha"]:,.0f} ha ({n["pct"]:.1f}%)</text>')

    # DESTAQUE DE TEXTO TÉCNICO SOBRE AS PRINCIPAIS TRANSIÇÕES NO MEIO
    svg.append(f'  <!-- Destaques centrais -->')
    mid_x = (x_left + node_w + x_right) / 2
    svg.append(f'  <rect x="{mid_x - 30.0:.2f}" y="{bottom_y - 6.0:.2f}" width="60.0" height="4.5" fill="#f8faf9" stroke="#cccccc" stroke-width="0.25" rx="0" ry="0" />')
    svg.append(f'  <text x="{mid_x:.2f}" y="{bottom_y - 2.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.0" fill="#1b3626" text-anchor="middle">43,1% Floresta Estável | 36,6% Água Estável | 2,7% Floresta → Pastagem</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Diagrama de Sankey gerado: {output_path}")

gerar_diagrama_sankey_academico("paineis_tematicos_svg/relatorio_diagrama_sankey.svg")
