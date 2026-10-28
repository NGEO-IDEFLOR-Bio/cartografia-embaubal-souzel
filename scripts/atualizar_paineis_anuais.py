# -*- coding: utf-8 -*-
"""
Atualização dos 5 Painéis Anuais (1985, 1995, 2005, 2015, 2024)
Ajuste solicitado pelo usuário:
- CIMA: Apenas PERCENTUAL (%) com barras horizontais limpas e números grandes.
- BAIXO: Apenas ÁREA EM HECTARES (ha) no quadro quantitativo, eliminando qualquer duplicidade.
- Zero letras miúdas, alto impacto visual.
Dimensões: 111.752 mm x 185.429 mm
"""

import pandas as pd
import os

df = pd.read_csv("camadas/tabelas/estatisticas_mapbiomas_c11_revis_rds.csv")

# Consolidado REVIS + RDS
df_tot = df.groupby(['Ano', 'Classe_ID', 'Classe_Nome'], as_index=False)['Area_ha'].sum()
tot_ano = df_tot.groupby('Ano')['Area_ha'].transform('sum')
df_tot['Percentual'] = (df_tot['Area_ha'] / tot_ano) * 100.0

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

W = 111.752
H = 185.429

def gerar_painel_anual_sem_duplicidade(ano, output_path):
    sub = df_tot[df_tot['Ano'] == ano].sort_values(by='Area_ha', ascending=False)
    area_tot = sub['Area_ha'].sum()
    
    # Classes principais (>= 0.1% ou top 5)
    classes_mostradas = [r for _, r in sub.iterrows() if r['Percentual'] >= 0.1][:5]
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">')
    svg.append(f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff" fill-opacity="0" />')

    # 1. BLOCO SUPERIOR: ANO EM DESTAQUE E ÁREA TOTAL
    svg.append(f'  <!-- Card Destaque Ano -->')
    svg.append(f'  <rect x="4.0" y="4.0" width="{W-8.0}" height="25.0" fill="#f4f7f5" stroke="#1b3626" stroke-width="0.8" rx="0" ry="0" />')
    svg.append(f'  <text x="8.0" y="14.0" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.2" fill="#666666">ANO DE REFERÊNCIA</text>')
    svg.append(f'  <text x="8.0" y="25.0" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="10.5" font-weight="bold" fill="#1b3626">{ano}</text>')
    
    svg.append(f'  <text x="{W-8.0}" y="14.0" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.6" fill="#777777" text-anchor="end">ÁREA MAPEADA</text>')
    svg.append(f'  <text x="{W-8.0}" y="23.5" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="5.4" font-weight="bold" fill="#222222" text-anchor="end">{area_tot:,.0f} ha</text>')

    # 2. SEÇÃO GRÁFICA SUPERIOR: APENAS PERCENTUAL (%)
    bar_section_y = 35.0
    svg.append(f'  <text x="4.0" y="{bar_section_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.8" font-weight="bold" fill="#1b3626">PROPORÇÃO DA COBERTURA (%)</text>')
    svg.append(f'  <line x1="4.0" y1="{bar_section_y + 2.5:.2f}" x2="{W-4.0}" y2="{bar_section_y + 2.5:.2f}" stroke="#cccccc" stroke-width="0.5" />')

    cur_y = bar_section_y + 8.5
    bar_max_w = W - 26.0  # Mais espaço para a barra pois não tem ha ao lado
    
    for r in classes_mostradas:
        cid = int(r['Classe_ID'])
        nome = CORES.get(cid, {}).get('nome', r['Classe_Nome'])
        cor = CORES.get(cid, {}).get('hex', '#888888')
        pct = r['Percentual']

        # Nome da classe à esquerda e grande percentual à direita
        svg.append(f'  <text x="4.0" y="{cur_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.2" font-weight="bold" fill="#222222">{nome}</text>')
        svg.append(f'  <text x="{W-4.0}" y="{cur_y:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.8" font-weight="bold" fill="#1b3626" text-anchor="end">{pct:.1f}%</text>')

        # Barra cinza de base (100%)
        bar_y = cur_y + 2.0
        svg.append(f'  <rect x="4.0" y="{bar_y:.2f}" width="{bar_max_w:.2f}" height="5.2" fill="#eaeeeb" rx="0" ry="0" />')
        
        # Barra de cor proporcional
        fill_w = max(1.8, (pct / 100.0) * bar_max_w)
        svg.append(f'  <rect x="4.0" y="{bar_y:.2f}" width="{fill_w:.2f}" height="5.2" fill="{cor}" stroke="#222222" stroke-width="0.25" rx="0" ry="0" />')

        cur_y += 12.8

    # 3. SEÇÃO INFERIOR: APENAS ÁREA EM HECTARES (ha)
    tab_y = cur_y + 3.0
    svg.append(f'  <line x1="4.0" y1="{tab_y:.2f}" x2="{W-4.0}" y2="{tab_y:.2f}" stroke="#cccccc" stroke-width="0.5" />')
    svg.append(f'  <text x="4.0" y="{tab_y + 6.0:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.8" font-weight="bold" fill="#1b3626">QUANTIFICAÇÃO TERRITORIAL (ha)</text>')

    # Cabeçalho da tabela de hectares
    head_y = tab_y + 9.5
    svg.append(f'  <rect x="4.0" y="{head_y:.2f}" width="{W-8.0}" height="6.0" fill="#e6ede8" rx="0" ry="0" />')
    svg.append(f'  <text x="7.0" y="{head_y + 4.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.9" font-weight="bold" fill="#222222">Classe de Cobertura</text>')
    svg.append(f'  <text x="{W-7.0}" y="{head_y + 4.2:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.9" font-weight="bold" fill="#1b3626" text-anchor="end">Área (ha)</text>')

    r_y = head_y + 6.0
    for r in classes_mostradas:
        cid = int(r['Classe_ID'])
        nome = CORES.get(cid, {}).get('nome', r['Classe_Nome'])
        cor = CORES.get(cid, {}).get('hex', '#888888')
        ha = r['Area_ha']

        # Quadrinho de cor da classe
        svg.append(f'  <rect x="6.0" y="{r_y + 1.5:.2f}" width="3.6" height="3.6" fill="{cor}" stroke="#222222" stroke-width="0.25" rx="0" ry="0" />')
        # Nome da classe
        svg.append(f'  <text x="12.0" y="{r_y + 4.3:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="2.9" fill="#222222">{nome}</text>')
        # Hectares grande e limpo à direita
        svg.append(f'  <text x="{W-7.0}" y="{r_y + 4.3:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.1" font-weight="bold" fill="#222222" text-anchor="end">{ha:,.0f} ha</text>')
        
        svg.append(f'  <line x1="4.0" y1="{r_y + 6.2:.2f}" x2="{W-4.0}" y2="{r_y + 6.2:.2f}" stroke="#eeeeee" stroke-width="0.3" />')
        r_y += 6.6

    # Linha Total (Hectares)
    svg.append(f'  <rect x="4.0" y="{r_y + 1.2:.2f}" width="{W-8.0}" height="7.0" fill="#f4f7f5" stroke="#1b3626" stroke-width="0.4" rx="0" ry="0" />')
    svg.append(f'  <text x="7.0" y="{r_y + 5.9:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.2" font-weight="bold" fill="#1b3626">ÁREA TOTAL</text>')
    svg.append(f'  <text x="{W-7.0}" y="{r_y + 5.9:.2f}" font-family="Segoe UI Variable Small Semibold, Segoe UI, sans-serif" font-size="3.4" font-weight="bold" fill="#1b3626" text-anchor="end">{area_tot:,.0f} ha</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"[OK] Painel Anual Atualizado (Sem Duplicidade): {output_path}")

for ano in [1985, 1995, 2005, 2015, 2024]:
    gerar_painel_anual_sem_duplicidade(ano, f"paineis_tematicos_svg/painel_mapa_ano_{ano}.svg")
