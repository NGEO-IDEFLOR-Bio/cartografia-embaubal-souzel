# -*- coding: utf-8 -*-
"""
Gera os gráficos SVG para os painéis dos Mapas de Análise Temporal de Uso e Cobertura do Solo.
Dimensões exatas solicitadas pelo usuário:
Largura: 111.752 mm
Altura: 185.429 mm
Fonte: Segoe UI Variable Small Semibold
Padrão: Qt SVG 1.2 Tiny compatível com QGIS Layout Picture Item (sem classes CSS, atributos diretos).
"""

import json
import os

with open("camadas/tabelas/estatisticas_mapbiomas_c11_ucs.json", encoding="utf-8") as f:
    dados_ucs = json.load(f)

# Classes e cores de destaque
CORES_DESTAQUE = {
    6:  {'nome': 'Floresta Alagável', 'cor': '#007785', 'borda': '#005560'},
    33: {'nome': 'Corpo Hídrico (Rio/Lago)', 'cor': '#2532e4', 'borda': '#1824b0'},
    11: {'nome': 'Campo Alagado / Pantanoso', 'cor': '#519799', 'borda': '#3e7678'},
    15: {'nome': 'Pastagem', 'cor': '#edde8e', 'borda': '#c5b66c'},
    21: {'nome': 'Mosaico de Usos', 'cor': '#ffefc3', 'borda': '#d9caa0'},
    3:  {'nome': 'Formação Florestal', 'cor': '#1f8d49', 'borda': '#146031'},
    12: {'nome': 'Formação Campestre', 'cor': '#d6bc74', 'borda': '#b29c5e'},
}

def gerar_svg_painel(uc_data, output_path):
    W = 111.752
    H = 185.429
    
    anos = [1985, 1995, 2005, 2015, 2024]
    
    # Identificar classes que têm pelo menos 0.5% em algum ano para a legenda
    classes_relevantes = {}
    for a in anos:
        info_ano = uc_data["anos"].get(str(a), {})
        for cl in info_ano.get("classes", []):
            if cl["percentual"] >= 0.4:
                classes_relevantes[cl["id"]] = cl["nome"]

    # Se forem poucas (ex: REVIS), garantir pelo menos as 3 principais
    if len(classes_relevantes) < 3:
        for a in anos:
            for cl in uc_data["anos"].get(str(a), {}).get("classes", []):
                classes_relevantes[cl["id"]] = cl["nome"]

    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">')
    
    # Fundo transparente ou card neutro
    svg_lines.append(f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff" fill-opacity="0" />')

    # CABEÇALHO DO PAINEL (Subtítulo técnico da UC)
    nome_curto = "REVIS TABULEIRO DO EMBAUBAL" if "Embaubal" in uc_data["unidade"] else "RDS VITÓRIA DE SOUZEL"
    area_total = uc_data["anos"]["2024"]["area_total_ha"]
    
    svg_lines.append(f'  <!-- Header info -->')
    svg_lines.append(f'  <text x="3.0" y="7.0" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.2" font-weight="bold" fill="#1b3626">{nome_curto}</text>')
    svg_lines.append(f'  <text x="3.0" y="11.2" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" fill="#555555">Área Total: {area_total:,.1f} ha | Coleção 11 (1985-2024)</text>')
    svg_lines.append(f'  <line x1="3.0" y1="13.5" x2="{W-3.0}" y2="13.5" stroke="#cccccc" stroke-width="0.35" />')

    # ÁREA DO GRÁFICO DE BARRAS EMPILHADAS (STACKED BARS)
    # Mostra a evolução 100% da área em cada ano chave
    chart_x = 14.0
    chart_y = 18.0
    chart_w = W - chart_x - 4.0  # ~93 mm
    chart_h = 70.0
    
    # Eixo Y (0%, 25%, 50%, 75%, 100%)
    for pct in [0, 25, 50, 75, 100]:
        y_pos = chart_y + chart_h - (pct / 100.0 * chart_h)
        svg_lines.append(f'  <line x1="{chart_x}" y1="{y_pos:.2f}" x2="{chart_x + chart_w}" y2="{y_pos:.2f}" stroke="#e5e5e5" stroke-width="0.3" stroke-dasharray="0.8,0.8" />')
        svg_lines.append(f'  <text x="{chart_x - 1.5}" y="{y_pos + 0.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.1" fill="#777777" text-anchor="end">{pct}%</text>')

    # Linha base
    svg_lines.append(f'  <line x1="{chart_x}" y1="{chart_y + chart_h}" x2="{chart_x + chart_w}" y2="{chart_y + chart_h}" stroke="#333333" stroke-width="0.5" />')

    # BARRAS POR ANO
    bar_width = 11.0
    spacing = (chart_w - (len(anos) * bar_width)) / (len(anos) + 1)
    
    for i, a in enumerate(anos):
        bx = chart_x + spacing + i * (bar_width + spacing)
        info_ano = uc_data["anos"].get(str(a), {})
        classes_ano = info_ano.get("classes", [])
        
        # Desenhar segmentos acumulados (do chão para cima)
        acum_y = chart_y + chart_h
        for cl in reversed(classes_ano):
            pct = cl["percentual"]
            seg_h = (pct / 100.0) * chart_h
            if seg_h > 0.05:
                top_y = acum_y - seg_h
                cor = cl["hex"]
                svg_lines.append(f'  <rect x="{bx:.2f}" y="{top_y:.2f}" width="{bar_width:.2f}" height="{seg_h:.2f}" fill="{cor}" stroke="#222222" stroke-width="0.15" rx="0" ry="0" />')
                # Rótulo de porcentagem no segmento se couber (altura >= 4.5mm)
                if seg_h >= 5.0 and pct >= 5.0:
                    text_color = "#ffffff" if cl["id"] in [6, 33, 11, 3] else "#111111"
                    svg_lines.append(f'  <text x="{bx + bar_width/2:.2f}" y="{top_y + seg_h/2 + 0.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.0" font-weight="bold" fill="{text_color}" text-anchor="middle">{pct:.0f}%</text>')
                acum_y = top_y

        # Rótulo do Ano abaixo da barra
        svg_lines.append(f'  <text x="{bx + bar_width/2:.2f}" y="{chart_y + chart_h + 3.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.4" font-weight="bold" fill="#333333" text-anchor="middle">{a}</text>')

    # DIVISÓRIA
    mid_y = chart_y + chart_h + 7.5
    svg_lines.append(f'  <line x1="3.0" y1="{mid_y:.2f}" x2="{W-3.0}" y2="{mid_y:.2f}" stroke="#cccccc" stroke-width="0.35" />')

    # TABELA COMPARATIVA RESUMIDA (1985 vs 2024)
    # Mostra a dinâmica de ganho/perda de área em hectares e %
    tab_y = mid_y + 4.5
    svg_lines.append(f'  <text x="3.0" y="{tab_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" font-weight="bold" fill="#1b3626">BALANÇO TEMPORAL (1985 → 2024)</text>')
    
    # Cabeçalho da tabela
    head_y = tab_y + 4.2
    svg_lines.append(f'  <rect x="3.0" y="{head_y - 2.8:.2f}" width="{W - 6.0}" height="3.8" fill="#f0f3f1" rx="0" ry="0" />')
    svg_lines.append(f'  <text x="5.0" y="{head_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.1" font-weight="bold" fill="#333333">Classe de Cobertura</text>')
    svg_lines.append(f'  <text x="{W - 35.0}" y="{head_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.1" font-weight="bold" fill="#333333" text-anchor="end">1985 (ha)</text>')
    svg_lines.append(f'  <text x="{W - 17.0}" y="{head_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.1" font-weight="bold" fill="#333333" text-anchor="end">2024 (ha)</text>')
    svg_lines.append(f'  <text x="{W - 4.5}" y="{head_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.1" font-weight="bold" fill="#333333" text-anchor="end">2024 %</text>')

    # Linhas das classes principais
    info_85 = {c["id"]: c for c in uc_data["anos"]["1985"]["classes"]}
    info_24 = {c["id"]: c for c in uc_data["anos"]["2024"]["classes"]}
    
    # Ordenar por relevância em 2024
    todas_ids = sorted(list(classes_relevantes.keys()), key=lambda cid: info_24.get(cid, {}).get("percentual", 0), reverse=True)
    
    row_y = head_y + 4.0
    for cid in todas_ids:
        cl_nome = classes_relevantes[cid]
        ha_85 = info_85.get(cid, {}).get("area_ha", 0.0)
        ha_24 = info_24.get(cid, {}).get("area_ha", 0.0)
        pct_24 = info_24.get(cid, {}).get("percentual", 0.0)
        cor = info_24.get(cid, {}).get("hex", "#888888")

        # Quadrinho de cor
        svg_lines.append(f'  <rect x="4.5" y="{row_y - 2.1:.2f}" width="2.4" height="2.4" fill="{cor}" stroke="#333333" stroke-width="0.15" rx="0" ry="0" />')
        # Nome da classe (encurtado se necessário)
        nome_display = cl_nome if len(cl_nome) <= 22 else cl_nome[:20] + "..."
        svg_lines.append(f'  <text x="8.0" y="{row_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.0" fill="#222222">{nome_display}</text>')
        # Valores
        svg_lines.append(f'  <text x="{W - 35.0}" y="{row_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.0" fill="#555555" text-anchor="end">{ha_85:,.0f}</text>')
        svg_lines.append(f'  <text x="{W - 17.0}" y="{row_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.0" font-weight="bold" fill="#222222" text-anchor="end">{ha_24:,.0f}</text>')
        svg_lines.append(f'  <text x="{W - 4.5}" y="{row_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.0" font-weight="bold" fill="#1b3626" text-anchor="end">{pct_24:.1f}%</text>')
        
        # Linha pontilhada suave abaixo da linha
        svg_lines.append(f'  <line x1="4.5" y1="{row_y + 1.2:.2f}" x2="{W - 4.5}" y2="{row_y + 1.2:.2f}" stroke="#eeeeee" stroke-width="0.25" />')
        row_y += 3.6

    # NOTA DE RODAPÉ METODOLÓGICA TÉCNICA
    nota_y = H - 5.5
    svg_lines.append(f'  <line x1="3.0" y1="{nota_y - 2.0:.2f}" x2="{W-3.0}" y2="{nota_y - 2.0:.2f}" stroke="#cccccc" stroke-width="0.3" />')
    svg_lines.append(f'  <text x="3.0" y="{nota_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="1.9" fill="#777777">Fonte: MapBiomas Brasil (Coleção 11, 30m). Processamento: IDEFLOR-Bio.</text>')
    svg_lines.append(f'  <text x="3.0" y="{nota_y + 2.8:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="1.9" fill="#777777">Cálculo zonal de pixels contidos no polígono oficial do Decreto de Criação.</text>')

    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Gerado: {output_path}")

# Gerar para REVIS e RDS
os.makedirs("paineis_tematicos_svg", exist_ok=True)

for uc in dados_ucs:
    if "Embaubal" in uc["unidade"]:
        out = "paineis_tematicos_svg/grafico_cobertura_revis_embaubal.svg"
        gerar_svg_painel(uc, out)
    elif "Vitória de Souzel" in uc["unidade"] or "Vitoria" in uc["unidade"]:
        out = "paineis_tematicos_svg/grafico_cobertura_rds_souzel.svg"
        gerar_svg_painel(uc, out)
