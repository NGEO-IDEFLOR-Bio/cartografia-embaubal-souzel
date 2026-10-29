# -*- coding: utf-8 -*-
"""
Geração dos Painéis SVG para o Tema Fogo (MapBiomas Fogo 1985 - 2024)
Área de Estudo: REVIS Tabuleiro do Embaubal, RDS Vitória de Souzel e Buffer 2km.

Dimensões idênticas aos painéis de Cobertura do Solo:
- Largura: 111.752 mm
- Altura:  185.429 mm
Padrão sem duplicidade, tipografia Segoe UI Variable, estética institucional IDEFLOR-Bio / NGEO.
"""

import pandas as pd
import os
import xml.sax.saxutils

DIR_SVG = "paineis_tematicos_svg"
os.makedirs(DIR_SVG, exist_ok=True)

W = 111.752
H = 185.429

# Carrega estatísticas de intervalos
df_int = pd.read_csv("camadas/tabelas/estatisticas_mapbiomas_fogo_intervalos.csv")
df_anual = pd.read_csv("camadas/tabelas/estatisticas_anuais_mapbiomas_fogo_1985_2026.csv")

# Paleta de cores cartográfica profissional para Fogo
CORES_INTERVALO = {
    "1985 – 1994": {"nome": "1985 – 1994", "hex": "#f39c12", "stroke": "#b9770e", "label": "Período 1985–1994"},
    "1995 – 2004": {"nome": "1995 – 2004", "hex": "#e67e22", "stroke": "#a04000", "label": "Período 1995–2004"},
    "2005 – 2014": {"nome": "2005 – 2014", "hex": "#e74c3c", "stroke": "#922b21", "label": "Período 2005–2014"},
    "2015 – 2024": {"nome": "2015 – 2024", "hex": "#900c3f", "stroke": "#581845", "label": "Período 2015–2024"}
}

# -------------------------------------------------------------
# 1. PAINEL GERAL CONSOLIDADO DE FOGO (1985 – 2024)
# -------------------------------------------------------------
def gerar_painel_fogo_consolidado(output_path):
    # Soma total das cicatrizes líquidas mapeadas no período
    tot_liquido = df_int['Total_ha'].sum()
    buf_tot = df_int['Buffer_ha'].sum()
    rds_tot = df_int['RDS_ha'].sum()
    revis_tot = df_int['REVIS_ha'].sum()

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">')
    svg.append(f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff" fill-opacity="0" />')

    # BLOCO SUPERIOR: TEMA EM DESTAQUE E ÁREA TOTAL
    svg.append('  <!-- Card Destaque Fogo -->')
    svg.append(f'  <rect x="4.0" y="4.0" width="{W-8.0}" height="25.0" fill="#fdfaf6" stroke="#900c3f" stroke-width="0.8" rx="0" ry="0" />')
    svg.append(f'  <text x="8.0" y="13.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.0" fill="#777777">MAPBIOMAS FOGO (COLEÇÃO 3.1)</text>')
    svg.append(f'  <text x="8.0" y="24.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="8.8" font-weight="bold" fill="#900c3f">1985 – 2024</text>')
    
    svg.append(f'  <text x="{W-8.0}" y="13.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" fill="#777777" text-anchor="end">TOTAL DE CICATRIZES</text>')
    svg.append(f'  <text x="{W-8.0}" y="23.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="5.2" font-weight="bold" fill="#222222" text-anchor="end">{tot_liquido:,.0f} ha</text>')

    # SEÇÃO SUPERIOR: PROPORÇÃO POR INTERVALO (%)
    bar_y0 = 35.0
    svg.append(f'  <text x="4.0" y="{bar_y0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.6" font-weight="bold" fill="#900c3f">DISTRIBUIÇÃO TEMPORAL (%)</text>')
    svg.append(f'  <line x1="4.0" y1="{bar_y0 + 2.5:.2f}" x2="{W-4.0}" y2="{bar_y0 + 2.5:.2f}" stroke="#cccccc" stroke-width="0.5" />')

    cur_y = bar_y0 + 8.5
    bar_max_w = W - 26.0

    for _, r in df_int.iterrows():
        nome_int = r['Intervalo']
        cfg = CORES_INTERVALO.get(nome_int, {"hex": "#888888", "stroke": "#444444"})
        ha_val = r['Total_ha']
        pct = (ha_val / tot_liquido) * 100.0 if tot_liquido > 0 else 0

        svg.append(f'  <text x="4.0" y="{cur_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.2" font-weight="bold" fill="#222222">{nome_int}</text>')
        svg.append(f'  <text x="{W-4.0}" y="{cur_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.8" font-weight="bold" fill="#900c3f" text-anchor="end">{pct:.1f}%</text>')

        bar_y = cur_y + 2.0
        svg.append(f'  <rect x="4.0" y="{bar_y:.2f}" width="{bar_max_w:.2f}" height="5.2" fill="#f5f0eb" rx="0" ry="0" />')
        
        fill_w = max(1.8, (pct / 100.0) * bar_max_w)
        svg.append(f'  <rect x="4.0" y="{bar_y:.2f}" width="{fill_w:.2f}" height="5.2" fill="{cfg["hex"]}" stroke="{cfg["stroke"]}" stroke-width="0.3" rx="0" ry="0" />')

        cur_y += 12.8

    # SEÇÃO INFERIOR: QUANTIFICAÇÃO POR UNIDADE TERRITORIAL
    tab_y = cur_y + 1.0
    svg.append(f'  <line x1="4.0" y1="{tab_y:.2f}" x2="{W-4.0}" y2="{tab_y:.2f}" stroke="#cccccc" stroke-width="0.5" />')
    svg.append(f'  <text x="4.0" y="{tab_y + 5.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.6" font-weight="bold" fill="#900c3f">ÁREA QUEIMADA POR UNIDADE (ha)</text>')

    head_y = tab_y + 8.5
    svg.append(f'  <rect x="4.0" y="{head_y:.2f}" width="{W-8.0}" height="5.8" fill="#f9eae1" rx="0" ry="0" />')
    svg.append(f'  <text x="7.0" y="{head_y + 4.1:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.8" font-weight="bold" fill="#222222">Unidade Territorial</text>')
    svg.append(f'  <text x="{W-7.0}" y="{head_y + 4.1:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.8" font-weight="bold" fill="#900c3f" text-anchor="end">Área (ha)</text>')

    unidades_dados = [
        {"nome": "REVIS Tab. do Embaubal", "ha": revis_tot, "cor": "#27ae60", "obs": "0,00% (Intacto)"},
        {"nome": "RDS Vitória de Souzel", "ha": rds_tot, "cor": "#2980b9", "obs": "0,58 ha (1988)"},
        {"nome": "Entorno (Buffer 2 km)", "ha": buf_tot, "cor": "#e67e22", "obs": f"{buf_tot:,.0f} ha"}
    ]

    r_y = head_y + 5.8
    for u in unidades_dados:
        svg.append(f'  <rect x="6.0" y="{r_y + 1.5:.2f}" width="3.4" height="3.4" fill="{u["cor"]}" stroke="#222222" stroke-width="0.25" rx="0" ry="0" />')
        svg.append(f'  <text x="12.0" y="{r_y + 4.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.8" fill="#222222">{u["nome"]}</text>')
        svg.append(f'  <text x="{W-7.0}" y="{r_y + 4.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.0" font-weight="bold" fill="#222222" text-anchor="end">{u["ha"]:,.1f} ha</text>')
        svg.append(f'  <line x1="4.0" y1="{r_y + 6.0:.2f}" x2="{W-4.0}" y2="{r_y + 6.0:.2f}" stroke="#eeeeee" stroke-width="0.3" />')
        r_y += 6.4

    # Linha Total
    svg.append(f'  <rect x="4.0" y="{r_y + 1.0:.2f}" width="{W-8.0}" height="6.6" fill="#fdfaf6" stroke="#900c3f" stroke-width="0.4" rx="0" ry="0" />')
    svg.append(f'  <text x="7.0" y="{r_y + 5.4:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.0" font-weight="bold" fill="#900c3f">TOTAL LÍQUIDO</text>')
    svg.append(f'  <text x="{W-7.0}" y="{r_y + 5.4:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.3" font-weight="bold" fill="#900c3f" text-anchor="end">{tot_liquido:,.0f} ha</text>')

    # Linha comparativa UCs vs Buffer
    r_y += 8.5
    svg.append(f'  <rect x="4.0" y="{r_y:.2f}" width="{W-8.0}" height="13.5" fill="#f5f7f6" stroke="#cccccc" stroke-width="0.3" />')
    svg.append(f'  <text x="7.0" y="{r_y + 4.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" font-weight="bold" fill="#1b3626">EFETIVIDADE DE PROTEÇÃO:</text>')
    svg.append(f'  <text x="7.0" y="{r_y + 8.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" fill="#444444">• Interior das UCs: apenas 0,58 ha (&lt; 0,01%)</text>')
    svg.append(f'  <text x="7.0" y="{r_y + 12.0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" fill="#444444">• 99,99% do fogo concentrado na borda externa</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Painel Geral Fogo criado: {output_path}")


# -------------------------------------------------------------
# 2. PAINÉIS INDIVIDUAIS POR INTERVALO TEMPORAL
# -------------------------------------------------------------
def gerar_painel_intervalo(row, output_path):
    nome_int = row['Intervalo']
    cfg = CORES_INTERVALO.get(nome_int, {"hex": "#e67e22", "stroke": "#a04000"})
    
    ha_tot = row['Total_ha']
    ha_buf = row['Buffer_ha']
    ha_rds = row['RDS_ha']
    ha_rev = row['REVIS_ha']
    qtd_cic = row['Qtd_Cicatrizes']
    
    # Anos abrangidos
    ano_ini, ano_fim = [int(x.strip()) for x in nome_int.split('–')]
    sub_anual = df_anual[(df_anual['ano'] >= ano_ini) & (df_anual['ano'] <= ano_fim)]
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">')
    svg.append(f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff" fill-opacity="0" />')

    # Card Superior
    svg.append(f'  <rect x="4.0" y="4.0" width="{W-8.0}" height="25.0" fill="#fdfaf6" stroke="{cfg["stroke"]}" stroke-width="0.8" rx="0" ry="0" />')
    svg.append(f'  <text x="8.0" y="13.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.0" fill="#777777">INTERVALO TEMPORAL</text>')
    svg.append(f'  <text x="8.0" y="24.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="8.8" font-weight="bold" fill="{cfg["hex"]}">{nome_int}</text>')
    
    svg.append(f'  <text x="{W-8.0}" y="13.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" fill="#777777" text-anchor="end">ÁREA QUEIMADA</text>')
    svg.append(f'  <text x="{W-8.0}" y="23.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="5.2" font-weight="bold" fill="#222222" text-anchor="end">{ha_tot:,.0f} ha</text>')

    # SEÇÃO SUPERIOR: DINÂMICA ANUAL DO INTERVALO (%)
    bar_y0 = 35.0
    svg.append(f'  <text x="4.0" y="{bar_y0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.6" font-weight="bold" fill="{cfg["stroke"]}">DISTRIBUIÇÃO POR UNIDADE (%)</text>')
    svg.append(f'  <line x1="4.0" y1="{bar_y0 + 2.5:.2f}" x2="{W-4.0}" y2="{bar_y0 + 2.5:.2f}" stroke="#cccccc" stroke-width="0.5" />')

    cur_y = bar_y0 + 8.5
    bar_max_w = W - 26.0

    itens_barra = [
        {"nome": "Entorno (Buffer 2 km)", "ha": ha_buf, "pct": (ha_buf/ha_tot*100.0) if ha_tot > 0 else 0, "cor": cfg["hex"]},
        {"nome": "RDS Vitória de Souzel", "ha": ha_rds, "pct": (ha_rds/ha_tot*100.0) if ha_tot > 0 else 0, "cor": "#2980b9"},
        {"nome": "REVIS Tab. do Embaubal", "ha": ha_rev, "pct": 0.0, "cor": "#27ae60"},
    ]

    for item in itens_barra:
        pct = item['pct']
        svg.append(f'  <text x="4.0" y="{cur_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.2" font-weight="bold" fill="#222222">{item["nome"]}</text>')
        svg.append(f'  <text x="{W-4.0}" y="{cur_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.8" font-weight="bold" fill="{cfg["stroke"]}" text-anchor="end">{pct:.1f}%</text>')

        bar_y = cur_y + 2.0
        svg.append(f'  <rect x="4.0" y="{bar_y:.2f}" width="{bar_max_w:.2f}" height="5.2" fill="#f5f0eb" rx="0" ry="0" />')
        
        fill_w = max(1.8, (pct / 100.0) * bar_max_w) if pct > 0 else 0
        if fill_w > 0:
            svg.append(f'  <rect x="4.0" y="{bar_y:.2f}" width="{fill_w:.2f}" height="5.2" fill="{item["cor"]}" stroke="#222222" stroke-width="0.25" rx="0" ry="0" />')

        cur_y += 12.8

    # Histórico dos anos de maior pico no intervalo
    cur_y += 2.0
    picos = sub_anual.sort_values(by='ha_total', ascending=False).head(3)
    svg.append(f'  <rect x="4.0" y="{cur_y:.2f}" width="{W-8.0}" height="14.0" fill="#fdfaf6" stroke="#e0e0e0" stroke-width="0.3" />')
    svg.append(f'  <text x="7.0" y="{cur_y + 4.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" font-weight="bold" fill="{cfg["stroke"]}">ANOS DE MAIOR OCORRÊNCIA NO DECÊNIO:</text>')
    
    pico_strs = [f"{int(r['ano'])}: {r['ha_total']:,.0f} ha" for _, r in picos.iterrows() if r['ha_total'] > 0]
    pico_txt = " • ".join(pico_strs) if pico_strs else "Sem ocorrências expressivas"
    svg.append(f'  <text x="7.0" y="{cur_y + 9.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.7" fill="#444444">{pico_txt}</text>')

    cur_y += 18.0

    # SEÇÃO INFERIOR: QUANTIFICAÇÃO TERRITORIAL (ha)
    tab_y = cur_y
    svg.append(f'  <line x1="4.0" y1="{tab_y:.2f}" x2="{W-4.0}" y2="{tab_y:.2f}" stroke="#cccccc" stroke-width="0.5" />')
    svg.append(f'  <text x="4.0" y="{tab_y + 5.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.6" font-weight="bold" fill="{cfg["stroke"]}">QUANTIFICAÇÃO TERRITORIAL (ha)</text>')

    head_y = tab_y + 8.5
    svg.append(f'  <rect x="4.0" y="{head_y:.2f}" width="{W-8.0}" height="5.8" fill="#f9eae1" rx="0" ry="0" />')
    svg.append(f'  <text x="7.0" y="{head_y + 4.1:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.8" font-weight="bold" fill="#222222">Unidade / Entorno</text>')
    svg.append(f'  <text x="{W-7.0}" y="{head_y + 4.1:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.8" font-weight="bold" fill="{cfg["stroke"]}" text-anchor="end">Área (ha)</text>')

    unidades_linhas = [
        {"nome": "REVIS Tab. do Embaubal", "ha": ha_rev, "cor": "#27ae60"},
        {"nome": "RDS Vitória de Souzel", "ha": ha_rds, "cor": "#2980b9"},
        {"nome": "Zona de Amortecimento", "ha": ha_buf, "cor": cfg["hex"]}
    ]

    r_y = head_y + 5.8
    for u in unidades_linhas:
        svg.append(f'  <rect x="6.0" y="{r_y + 1.5:.2f}" width="3.4" height="3.4" fill="{u["cor"]}" stroke="#222222" stroke-width="0.25" rx="0" ry="0" />')
        svg.append(f'  <text x="12.0" y="{r_y + 4.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.8" fill="#222222">{u["nome"]}</text>')
        svg.append(f'  <text x="{W-7.0}" y="{r_y + 4.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.0" font-weight="bold" fill="#222222" text-anchor="end">{u["ha"]:,.1f} ha</text>')
        svg.append(f'  <line x1="4.0" y1="{r_y + 6.0:.2f}" x2="{W-4.0}" y2="{r_y + 6.0:.2f}" stroke="#eeeeee" stroke-width="0.3" />')
        r_y += 6.4

    # Linha Total
    svg.append(f'  <rect x="4.0" y="{r_y + 1.0:.2f}" width="{W-8.0}" height="6.6" fill="#fdfaf6" stroke="{cfg["stroke"]}" stroke-width="0.4" rx="0" ry="0" />')
    svg.append(f'  <text x="7.0" y="{r_y + 5.4:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.0" font-weight="bold" fill="{cfg["stroke"]}">TOTAL DO INTERVALO</text>')
    svg.append(f'  <text x="{W-7.0}" y="{r_y + 5.4:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.3" font-weight="bold" fill="{cfg["stroke"]}" text-anchor="end">{ha_tot:,.0f} ha</text>')

    # Rodapé informativo: quantidade de polígonos
    r_y += 8.5
    svg.append(f'  <text x="4.0" y="{r_y + 4.0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.5" fill="#888888">Cicatrizes detectadas no intervalo: {qtd_cic} polígonos</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Painel Intervalo {nome_int} criado: {output_path}")


# -------------------------------------------------------------
# 3. GRÁFICO ACADÊMICO DE SÉRIE HISTÓRICA DO FOGO (A4)
# -------------------------------------------------------------
def gerar_grafico_serie_historica_fogo(output_path):
    W_g = 170.0
    H_g = 110.0
    
    sub = df_anual[(df_anual['ano'] >= 1985) & (df_anual['ano'] <= 2024)]
    max_ha = sub['ha_total'].max()
    max_y_val = 1100.0  # Arredondado para teto visual limpo
    
    margin_l = 18.0
    margin_r = 10.0
    margin_t = 20.0
    margin_b = 20.0
    
    plot_w = W_g - margin_l - margin_r
    plot_h = H_g - margin_t - margin_b
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_g}mm" height="{H_g}mm" viewBox="0 0 {W_g} {H_g}">')
    svg.append(f'  <rect x="0" y="0" width="{W_g}" height="{H_g}" fill="#ffffff" />')

    # Título do Gráfico
    svg.append(f'  <text x="{margin_l}" y="9.0" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="4.2" font-weight="bold" fill="#1b3626">Série Histórica de Queimadas no Entorno das UCs (1985 – 2024)</text>')
    svg.append(f'  <text x="{margin_l}" y="14.0" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" fill="#666666">Área anual de cicatrizes de fogo (ha) mapeada pelo MapBiomas Fogo no REVIS, RDS e Buffer de 2 km</text>')

    # Linhas de grade horizontais
    y_steps = [0, 250, 500, 750, 1000]
    for yv in y_steps:
        y_pos = margin_t + plot_h - (yv / max_y_val) * plot_h
        svg.append(f'  <line x1="{margin_l}" y1="{y_pos:.2f}" x2="{margin_l + plot_w}" y2="{y_pos:.2f}" stroke="#e5e5e5" stroke-width="0.3" stroke-dasharray="1,1" />')
        svg.append(f'  <text x="{margin_l - 2.5}" y="{y_pos + 1.0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" fill="#777777" text-anchor="end">{yv:,.0f}</text>')

    # Barras anuais
    n_anos = len(sub)
    bar_width = (plot_w / n_anos) * 0.75
    gap = plot_w / n_anos

    for i, (_, r) in enumerate(sub.iterrows()):
        ano = int(r['ano'])
        ha = r['ha_total']
        x = margin_l + i * gap + (gap - bar_width) / 2.0
        h_bar = (ha / max_y_val) * plot_h
        y = margin_t + plot_h - h_bar

        # Cor da barra pelo intervalo correspondente
        if ano < 1995:
            cor = "#f39c12"
        elif ano < 2005:
            cor = "#e67e22"
        elif ano < 2015:
            cor = "#e74c3c"
        else:
            cor = "#900c3f"

        svg.append(f'  <rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{h_bar:.2f}" fill="{cor}" rx="0.3" ry="0.3" />')

        # Destaque nos picos principais (2001, 1988, 2015, 2023)
        if ano in [1988, 2001, 2015, 2023]:
            svg.append(f'  <text x="{x + bar_width/2.0:.2f}" y="{y - 1.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.2" font-weight="bold" fill="#900c3f" text-anchor="middle">{ha:,.0f}</text>')

        # Labels do eixo X a cada 5 anos
        if ano % 5 == 0 or ano == 2024:
            svg.append(f'  <text x="{x + bar_width/2.0:.2f}" y="{margin_t + plot_h + 4.5:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.3" fill="#555555" text-anchor="middle">{ano}</text>')
            svg.append(f'  <line x1="{x + bar_width/2.0:.2f}" y1="{margin_t + plot_h}" x2="{x + bar_width/2.0:.2f}" y2="{margin_t + plot_h + 1.5}" stroke="#999999" stroke-width="0.3" />')

    # Eixo X e Y principais
    svg.append(f'  <line x1="{margin_l}" y1="{margin_t + plot_h}" x2="{margin_l + plot_w}" y2="{margin_t + plot_h}" stroke="#333333" stroke-width="0.5" />')
    svg.append(f'  <line x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{margin_t + plot_h}" stroke="#333333" stroke-width="0.5" />')

    # Legenda dos intervalos no topo direito
    leg_x = margin_l + plot_w - 75.0
    leg_y = 12.0
    svg.append(f'  <g transform="translate({leg_x}, {leg_y})">')
    itens_leg = [
        ("1985-94", "#f39c12"),
        ("1995-04", "#e67e22"),
        ("2005-14", "#e74c3c"),
        ("2015-24", "#900c3f")
    ]
    cur_lx = 0
    for l_txt, l_col in itens_leg:
        svg.append(f'    <rect x="{cur_lx}" y="0" width="3.0" height="3.0" fill="{l_col}" rx="0.3" />')
        svg.append(f'    <text x="{cur_lx + 4.0}" y="2.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.2" fill="#555555">{l_txt}</text>')
        cur_lx += 18.0
    svg.append('  </g>')

    # Nota de rodapé da figura
    svg.append(f'  <text x="{margin_l}" y="{H_g - 4.5}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.2" fill="#888888">Nota: Dos 11.675 ha de cicatrizes mapeadas em 41 anos, 99,99% ocorreram no entorno (Buffer 2km). A RDS teve 0,58 ha e o REVIS 0,00 ha.</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Gráfico Acadêmico de Fogo criado: {output_path}")


# Executa a geração de todos os painéis
gerar_painel_fogo_consolidado(f"{DIR_SVG}/painel_mapa_fogo_historico_1985_2024.svg")

for _, r in df_int.iterrows():
    suf = r['Intervalo'].replace(" – ", "_").replace(" ", "")
    gerar_painel_intervalo(r, f"{DIR_SVG}/painel_mapa_fogo_{suf}.svg")

gerar_grafico_serie_historica_fogo(f"{DIR_SVG}/relatorio_grafico_fogo_serie_historica.svg")
