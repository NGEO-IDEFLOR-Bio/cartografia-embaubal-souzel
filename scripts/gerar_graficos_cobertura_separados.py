# -*- coding: utf-8 -*-
"""
Geração dos Gráficos Acadêmicos de Uso e Cobertura da Terra (MapBiomas Coleção 11)
Separados por Unidade de Conservação:
1. REVIS Tabuleiro do Embaubal (4.035,71 ha)
2. RDS Vitória de Souzel (22.987,41 ha)
3. Painel Comparativo Integrado das Duas UCs

Padrão: 170 x 110 mm, barras empilhadas 100%, legenda lateral detalhada com valores de 2024.
"""

import pandas as pd
import os

DIR_SVG = "paineis_tematicos_svg"
os.makedirs(DIR_SVG, exist_ok=True)

df = pd.read_csv("camadas/tabelas/estatisticas_mapbiomas_c11_revis_rds.csv")

CORES = {
    6:  {'nome': 'Floresta Alagável', 'hex': '#007785'},
    33: {'nome': 'Rio, Lago e Oceano', 'hex': '#2532e4'},
    11: {'nome': 'Campo Alagado / Pantanoso', 'hex': '#519799'},
    15: {'nome': 'Pastagem', 'hex': '#edde8e'},
    21: {'nome': 'Mosaico de Usos', 'hex': '#ffefc3'},
    3:  {'nome': 'Formação Florestal', 'hex': '#1f8d49'},
    12: {'nome': 'Formação Campestre', 'hex': '#d6bc74'},
    4:  {'nome': 'Formação Savânica', 'hex': '#7dc975'},
    25: {'nome': 'Outras Áreas não Veg.', 'hex': '#db4d4f'},
}

ANOS = [1985, 1995, 2005, 2015, 2024]

# -------------------------------------------------------------
# 1. FUNÇÃO GERADORA DE GRÁFICO INDIVIDUAL DE COBERTURA
# -------------------------------------------------------------
def gerar_grafico_cobertura_unidade(filtro_uc, nome_titulo, subtitulo_txt, area_ha_total, classes_legenda, output_path):
    W = 170.0
    H = 110.0
    
    sub_df = df[df['Unidade'].str.contains(filtro_uc, case=False, na=False)].copy()
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">')
    svg.append(f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff" stroke="#dddddd" stroke-width="0.4" rx="0" ry="0" />')

    # Título Acadêmico da Figura
    svg.append(f'  <text x="8.0" y="9.0" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.8" font-weight="bold" fill="#1b3626">{nome_titulo}</text>')
    svg.append(f'  <text x="8.0" y="13.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" fill="#666666">{subtitulo_txt}</text>')
    svg.append(f'  <line x1="8.0" y1="16.0" x2="{W-8.0}" y2="16.0" stroke="#cccccc" stroke-width="0.4" />')

    # Área do Gráfico
    cx = 20.0
    cy = 22.0
    cw = 96.0
    ch = 68.0

    # Grid Y (0 a 100%)
    for pct in [0, 20, 40, 60, 80, 100]:
        y_p = cy + ch - (pct / 100.0 * ch)
        svg.append(f'  <line x1="{cx}" y1="{y_p:.2f}" x2="{cx + cw}" y2="{y_p:.2f}" stroke="#e5e5e5" stroke-width="0.3" stroke-dasharray="1.0,1.0" />')
        svg.append(f'  <text x="{cx - 2.0}" y="{y_p + 1.0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" fill="#666666" text-anchor="end">{pct}%</text>')

    svg.append(f'  <line x1="{cx}" y1="{cy + ch}" x2="{cx + cw}" y2="{cy + ch}" stroke="#333333" stroke-width="0.6" />')

    # Barras empilhadas por ano
    bw = 13.0
    gap = (cw - len(ANOS)*bw) / (len(ANOS) + 1)

    for i, a in enumerate(ANOS):
        bx = cx + gap + i * (bw + gap)
        sub_a = sub_df[sub_df['Ano'] == a]
        pct_map = dict(zip(sub_a['Classe_ID'], sub_a['Percentual']))

        acum_y = cy + ch
        # Ordem de empilhamento de baixo para cima
        for cid in [33, 6, 11, 15, 21, 12, 3]:
            pct = pct_map.get(cid, 0.0)
            if pct <= 0.05: continue
            sh = (pct / 100.0) * ch
            ty = acum_y - sh
            cor = CORES.get(cid, {}).get('hex', '#888888')
            svg.append(f'  <rect x="{bx:.2f}" y="{ty:.2f}" width="{bw:.2f}" height="{sh:.2f}" fill="{cor}" stroke="#222222" stroke-width="0.25" rx="0" ry="0" />')
            
            # Rótulo de percentual dentro da fatia se houver espaço
            if sh >= 5.2 and pct >= 5.0:
                tc = "#ffffff" if cid in [33, 6] else "#111111"
                svg.append(f'  <text x="{bx + bw/2:.2f}" y="{ty + sh/2 + 0.9:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.5" font-weight="bold" fill="{tc}" text-anchor="middle">{pct:.0f}%</text>')
            acum_y = ty

        svg.append(f'  <text x="{bx + bw/2:.2f}" y="{cy + ch + 4.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.9" font-weight="bold" fill="#222222" text-anchor="middle">{a}</text>')

    # Legenda Lateral Direita
    lx = cx + cw + 6.0
    ly = cy + 3.0
    svg.append(f'  <text x="{lx}" y="{ly:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.8" font-weight="bold" fill="#1b3626">LEGENDA (2024)</text>')
    
    ly += 5.0
    sub_2024 = sub_df[sub_df['Ano'] == 2024]
    
    for cid in classes_legenda:
        cor = CORES.get(cid, {}).get('hex', '#888888')
        nome = CORES.get(cid, {}).get('nome', f"Classe {cid}")
        
        row_c = sub_2024[sub_2024['Classe_ID'] == cid]
        if len(row_c) > 0:
            h24 = row_c['Area_ha'].values[0]
            p24 = row_c['Percentual'].values[0]
            val_txt = f"{h24:,.0f} ha ({p24:.1f}%)" if h24 >= 10 else f"{h24:.1f} ha ({p24:.2f}%)"
        else:
            val_txt = "0 ha (0,0%)"

        # Quadrinho de cor
        svg.append(f'  <rect x="{lx}" y="{ly:.2f}" width="3.8" height="3.8" fill="{cor}" stroke="#222222" stroke-width="0.25" rx="0" ry="0" />')
        svg.append(f'  <text x="{lx + 5.2}" y="{ly + 3.0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.2" font-weight="bold" fill="#333333">{nome}</text>')
        svg.append(f'  <text x="{lx + 5.2}" y="{ly + 6.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.0" fill="#666666">2024: {val_txt}</text>')
        ly += 9.5

    # Rodapé Técnico
    svg.append(f'  <line x1="8.0" y1="{H-8.0}" x2="{W-8.0}" y2="{H-8.0}" stroke="#cccccc" stroke-width="0.3" />')
    svg.append(f'  <text x="8.0" y="{H-4.5}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.1" fill="#777777">Fonte: MapBiomas Brasil (Coleção 11, 30m). Processamento: IDEFLOR-Bio / NGEO / DGMUC (2026).</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Gráfico gerado com sucesso: {output_path}")


# -------------------------------------------------------------
# 2. FUNÇÃO COMPARATIVA: AS DUAS UCS LADO A LADO EM UMA FIGURA (A4)
# -------------------------------------------------------------
def gerar_grafico_cobertura_comparativo_duas_ucs(output_path):
    W = 185.0
    H = 115.0
    
    sub_rev = df[df['Unidade'].str.contains('Embaubal')].copy()
    sub_rds = df[df['Unidade'].str.contains('Vit')].copy()

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">')
    svg.append(f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff" stroke="#dddddd" stroke-width="0.4" rx="0" ry="0" />')

    # Título
    svg.append(f'  <text x="8.0" y="8.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="4.0" font-weight="bold" fill="#1b3626">Evolução Comparativa do Uso e Cobertura da Terra (1985 – 2024)</text>')
    svg.append(f'  <text x="8.0" y="12.8" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.5" fill="#666666">Comparação entre o REVIS Tabuleiro do Embaubal (4.036 ha) e a RDS Vitória de Souzel (22.987 ha)</text>')
    svg.append(f'  <line x1="8.0" y1="15.2" x2="{W-8.0}" y2="15.2" stroke="#cccccc" stroke-width="0.4" />')

    # Parâmetros dos dois subplots
    pw = 58.0
    ph = 66.0
    py = 23.0
    
    # Subplot 1: REVIS (Esquerda)
    px1 = 18.0
    svg.append(f'  <text x="{px1}" y="{py - 2.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.9" font-weight="bold" fill="#27ae60">A) REVIS Tabuleiro do Embaubal</text>')
    
    # Grid Y REVIS
    for pct in [0, 20, 40, 60, 80, 100]:
        yp = py + ph - (pct / 100.0 * ph)
        svg.append(f'  <line x1="{px1}" y1="{yp:.2f}" x2="{px1 + pw}" y2="{yp:.2f}" stroke="#e5e5e5" stroke-width="0.3" stroke-dasharray="1.0,1.0" />')
        svg.append(f'  <text x="{px1 - 2.0}" y="{yp + 1.0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.2" fill="#666666" text-anchor="end">{pct}%</text>')
    svg.append(f'  <line x1="{px1}" y1="{py + ph}" x2="{px1 + pw}" y2="{py + ph}" stroke="#333333" stroke-width="0.5" />')

    bw = 8.5
    gap = (pw - len(ANOS)*bw) / (len(ANOS) + 1)
    for i, a in enumerate(ANOS):
        bx = px1 + gap + i * (bw + gap)
        sub_a = sub_rev[sub_rev['Ano'] == a]
        pct_map = dict(zip(sub_a['Classe_ID'], sub_a['Percentual']))
        acum_y = py + ph
        for cid in [33, 6, 11, 15, 21]:
            pct = pct_map.get(cid, 0.0)
            if pct <= 0.05: continue
            sh = (pct / 100.0) * ph
            ty = acum_y - sh
            cor = CORES.get(cid, {}).get('hex', '#888888')
            svg.append(f'  <rect x="{bx:.2f}" y="{ty:.2f}" width="{bw:.2f}" height="{sh:.2f}" fill="{cor}" stroke="#222222" stroke-width="0.2" />')
            if sh >= 4.5 and pct >= 8.0:
                tc = "#ffffff" if cid in [33, 6] else "#111111"
                svg.append(f'  <text x="{bx + bw/2:.2f}" y="{ty + sh/2 + 0.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.2" font-weight="bold" fill="{tc}" text-anchor="middle">{pct:.0f}%</text>')
            acum_y = ty
        svg.append(f'  <text x="{bx + bw/2:.2f}" y="{py + ph + 4.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.5" font-weight="bold" fill="#222222" text-anchor="middle">{a}</text>')

    # Subplot 2: RDS (Centro)
    px2 = px1 + pw + 15.0
    svg.append(f'  <text x="{px2}" y="{py - 2.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.9" font-weight="bold" fill="#e67e22">B) RDS Vitória de Souzel</text>')
    
    # Grid Y RDS
    for pct in [0, 20, 40, 60, 80, 100]:
        yp = py + ph - (pct / 100.0 * ph)
        svg.append(f'  <line x1="{px2}" y1="{yp:.2f}" x2="{px2 + pw}" y2="{yp:.2f}" stroke="#e5e5e5" stroke-width="0.3" stroke-dasharray="1.0,1.0" />')
    svg.append(f'  <line x1="{px2}" y1="{py + ph}" x2="{px2 + pw}" y2="{py + ph}" stroke="#333333" stroke-width="0.5" />')

    for i, a in enumerate(ANOS):
        bx = px2 + gap + i * (bw + gap)
        sub_a = sub_rds[sub_rds['Ano'] == a]
        pct_map = dict(zip(sub_a['Classe_ID'], sub_a['Percentual']))
        acum_y = py + ph
        for cid in [33, 6, 11, 15, 21, 12, 3]:
            pct = pct_map.get(cid, 0.0)
            if pct <= 0.05: continue
            sh = (pct / 100.0) * ph
            ty = acum_y - sh
            cor = CORES.get(cid, {}).get('hex', '#888888')
            svg.append(f'  <rect x="{bx:.2f}" y="{ty:.2f}" width="{bw:.2f}" height="{sh:.2f}" fill="{cor}" stroke="#222222" stroke-width="0.2" />')
            if sh >= 4.5 and pct >= 8.0:
                tc = "#ffffff" if cid in [33, 6] else "#111111"
                svg.append(f'  <text x="{bx + bw/2:.2f}" y="{ty + sh/2 + 0.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.2" font-weight="bold" fill="{tc}" text-anchor="middle">{pct:.0f}%</text>')
            acum_y = ty
        svg.append(f'  <text x="{bx + bw/2:.2f}" y="{py + ph + 4.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.5" font-weight="bold" fill="#222222" text-anchor="middle">{a}</text>')

    # Legenda Unificada à Direita
    lx = px2 + pw + 6.0
    ly = py + 2.0
    svg.append(f'  <text x="{lx}" y="{ly:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.7" font-weight="bold" fill="#1b3626">LEGENDA</text>')
    
    ly += 5.0
    for cid in [33, 6, 11, 15, 21]:
        cor = CORES[cid]['hex']
        nome = CORES[cid]['nome']
        svg.append(f'  <rect x="{lx}" y="{ly:.2f}" width="3.6" height="3.6" fill="{cor}" stroke="#222222" stroke-width="0.2" />')
        svg.append(f'  <text x="{lx + 5.0}" y="{ly + 2.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.1" fill="#333333">{nome}</text>')
        ly += 7.5

    # Rodapé
    svg.append(f'  <line x1="8.0" y1="{H-8.0}" x2="{W-8.0}" y2="{H-8.0}" stroke="#cccccc" stroke-width="0.3" />')
    svg.append(f'  <text x="8.0" y="{H-4.5}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.1" fill="#777777">Fonte: MapBiomas Brasil (Coleção 11, 30m). Processamento: IDEFLOR-Bio / NGEO / DGMUC (2026).</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Gráfico Comparativo de Cobertura gerado: {output_path}")


# -------------------------------------------------------------
# EXECUÇÃO DA GERAÇÃO
# -------------------------------------------------------------

# 1. Gráfico Individual REVIS Tabuleiro do Embaubal
gerar_grafico_cobertura_unidade(
    filtro_uc='Embaubal',
    nome_titulo='Evolução Temporal do Uso e Cobertura: REVIS Tabuleiro do Embaubal',
    subtitulo_txt='Refúgio de Vida Silvestre Tabuleiro do Embaubal (Área Legal: 4.035,71 ha)',
    area_ha_total=4035.71,
    classes_legenda=[33, 6, 11, 15, 21],
    output_path=f"{DIR_SVG}/relatorio_grafico_cobertura_revis_embaubal.svg"
)

# 2. Gráfico Individual RDS Vitória de Souzel
gerar_grafico_cobertura_unidade(
    filtro_uc='Vit',
    nome_titulo='Evolução Temporal do Uso e Cobertura: RDS Vitória de Souzel',
    subtitulo_txt='Reserva de Desenvolvimento Sustentável Vitória de Souzel (Área Legal: 22.987,41 ha)',
    area_ha_total=22987.41,
    classes_legenda=[6, 33, 11, 15, 21, 12, 3],
    output_path=f"{DIR_SVG}/relatorio_grafico_cobertura_rds_vitoria_souzel.svg"
)

# 3. Gráfico Comparativo Integrado das Duas UCs
gerar_grafico_cobertura_comparativo_duas_ucs(
    output_path=f"{DIR_SVG}/relatorio_grafico_cobertura_comparativo_ucs.svg"
)
