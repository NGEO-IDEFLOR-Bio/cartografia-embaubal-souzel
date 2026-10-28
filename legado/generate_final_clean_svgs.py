import os

output_dir = "paineis_tematicos_svg"
os.makedirs(output_dir, exist_ok=True)

FONT = "Segoe UI Variable Small Semibold, Segoe UI Semibold, Segoe UI, Arial"

def make_bar_chart_svg(items, max_val=None, val_suffix="%", round_digits=2):
    w, h = 136.382, 186.572
    margin_x = 7.0
    usable_w = w - (margin_x * 2) # ~122.38 mm
    
    if max_val is None:
        max_val = max(v for _, v, _ in items) * 1.15
        if max_val == 0: max_val = 1
        
    start_y = 10.0
    row_h = (h - start_y - 8.0) / len(items)
    bar_h = min(row_h * 0.42, 6.5)
    
    svg = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff" stroke="none" />''']
    
    for i, (name, val, col) in enumerate(items):
        y = start_y + (i * row_h)
        # 1. Label text (large, clear)
        label_size = min(row_h * 0.28, 3.6)
        svg.append(f'''  <text x="{margin_x:.2f}" y="{y + label_size:.2f}" font-family="{FONT}" font-size="{label_size:.2f}" font-weight="600" fill="#2c3e50">{name}</text>''')
        
        # 2. Track background bar
        bar_y = y + label_size + 2.0
        svg.append(f'''  <rect x="{margin_x:.2f}" y="{bar_y:.2f}" width="{usable_w:.2f}" height="{bar_h:.2f}" fill="#f1f3f5" rx="1.5" ry="1.5" />''')
        
        # 3. Colored bar
        bar_w = (val / max_val) * usable_w
        if bar_w < 3.5:
            bar_w = 3.5
        svg.append(f'''  <rect x="{margin_x:.2f}" y="{bar_y:.2f}" width="{bar_w:.2f}" height="{bar_h:.2f}" fill="{col}" rx="1.5" ry="1.5" />''')
        
        # 4. Value label
        if round_digits == 0:
            val_str = f"{int(val)}{val_suffix}"
        else:
            val_str = f"{val:.{round_digits}f}{val_suffix}".replace('.', ',')
            
        val_size = min(bar_h * 0.65, 3.2)
        text_x = margin_x + bar_w + 2.5
        text_anchor = "start"
        val_color = "#2c3e50"
        
        if text_x + 16.0 > margin_x + usable_w:
            text_x = margin_x + bar_w - 2.5
            text_anchor = "end"
            val_color = "#ffffff" if col in ["#574b90", "#55a368", "#8296c4", "#0d47a1", "#1b5e20", "#2b8a3e", "#0077b6"] else "#2c3e50"
            
        svg.append(f'''  <text x="{text_x:.2f}" y="{bar_y + bar_h*0.72:.2f}" font-family="{FONT}" font-size="{val_size:.2f}" font-weight="600" fill="{val_color}" text-anchor="{text_anchor}">{val_str}</text>''')

    svg.append('</svg>')
    return "\n".join(svg)


# ------------------------------------------------------------------------------
# 00. GRÁFICO IDÊNTICO AO MODELO DO USUÁRIO: REGIÕES DE INTEGRAÇÃO DO PARÁ (%)
# ------------------------------------------------------------------------------
regioes_para = [
    ("Baixo Amazonas", 25.35, "#8296c4"),
    ("Xingu", 20.13, "#f8a5c2"),
    ("Tapajós", 15.22, "#c6f1a8"),
    ("Araguaia", 13.98, "#9bf4d5"),
    ("Marajó", 8.56, "#fce38a"),
    ("Rio Capim", 4.99, "#d6a2e8"),
    ("Carajás", 3.59, "#f3a683"),
    ("Lago de Tucuruí", 3.20, "#63cdda"),
    ("Tocantins", 2.57, "#55a368"),
    ("Rio Caeté", 1.34, "#f5cd79"),
    ("Guamá", 0.93, "#a3cb38"),
    ("Guajará", 0.15, "#574b90")
]

# ------------------------------------------------------------------------------
# 01. LIMITES E UCs: ÁREA POR UNIDADE E USO NO MOSAICO (%)
# ------------------------------------------------------------------------------
tema_01_items = [
    ("RDS Vitória de Souzel (Manejo Sustentável)", 85.06, "#2b8a3e"),
    ("REVIS Tabuleiro do Embaubal (Proteção Integral)", 14.94, "#e65100"),
    ("Florestas de Várzea e Ilhas Aluviais", 62.40, "#55a368"),
    ("Espelho d'Água (Calha do Xingu e Rios)", 24.80, "#63cdda"),
    ("Praias Fluviais e Bancos de Areia", 7.20, "#fce38a"),
    ("Áreas de Uso Comunitário Tradicional", 5.60, "#f3a683")
]

# ------------------------------------------------------------------------------
# 02. GESTÃO E INFRAESTRUTURA: PONTOS DE CONTROLE E OPERAÇÃO (Qtd)
# ------------------------------------------------------------------------------
tema_02_items = [
    ("Trajetos Fluviais e Rotas de Patrulhamento", 49, "#5f3dc4"),
    ("Equipamentos Públicos e Estruturas", 19, "#0d47a1"),
    ("Pontos de Comunicação e Apoio Local", 12, "#63cdda"),
    ("Portos e Entradas Estratégicas", 8, "#2b8a3e"),
    ("Alertas e Ocorrências Ambientais (Fogo/Búfalos)", 7, "#c92a2a"),
    ("Pontos de Sinalização Náutica (Farol/Canais)", 5, "#f5cd79"),
    ("Captação de Água Doce / Poços Comunitários", 3, "#8296c4")
]

# ------------------------------------------------------------------------------
# 03. BIODIVERSIDADE: INVENTÁRIO DE QUELÔNIOS E RECURSOS VIVOS (Qtd)
# ------------------------------------------------------------------------------
tema_03_items = [
    ("Flora Nativa e Árvores Matrizes Protegidas", 50, "#2b8a3e"),
    ("Tabuleiros de Desova de Quelônios Mapeados", 22, "#007f5f"),
    ("Pontos de Postura da Tartaruga-da-amazônia", 18, "#d48b00"),
    ("Registros de Desova de Tracajá e Pitiú", 15, "#a3cb38"),
    ("Locais de Desova de Ictiofauna (Curimatá)", 4, "#63cdda"),
    ("Refúgios Mapeados de Peixe-boi da Amazônia", 2, "#8296c4")
]

# ------------------------------------------------------------------------------
# 04. COMUNIDADES E USO TRADICIONAL: ESTRUTURAS ANTRÓPICAS (Qtd)
# ------------------------------------------------------------------------------
tema_04_items = [
    ("Residências Ribeirinhas Permanentes", 282, "#e65100"),
    ("Ranchos de Apoio de Pesca Artesanal", 89, "#00838f"),
    ("Comunidades e Vilas Concentradoras", 12, "#2b8a3e"),
    ("Polos Escolares do Campo e Capelas", 6, "#5f3dc4"),
    ("Pontos de Pesca de Subsistência Ativos", 45, "#63cdda"),
    ("Áreas de Extrativismo Vegetal Tradicional", 28, "#55a368")
]

# ------------------------------------------------------------------------------
# 05. GEOGRAFIA E HIDROGRAFIA: FEIÇÕES DA BACIA E ARQUIPÉLAGO (Qtd)
# ------------------------------------------------------------------------------
tema_05_items = [
    ("Ilhas Fluviais do Arquipélago do Xingu", 55, "#b07d4b"),
    ("Furos Fluviais de Ligação e Atalhos", 33, "#0077b6"),
    ("Igarapés de Várzea e Drenagem Florestal", 28, "#55a368"),
    ("Rios Principais e Braços Navegáveis", 27, "#63cdda"),
    ("Praias Fluviais e Bancos de Areia Sazonais", 23, "#fce38a"),
    ("Marcos Náuticos, Bocas de Furos e Canais", 16, "#495057"),
    ("Lagos e Ressacos de Remanso de Várzea", 7, "#8296c4")
]

all_svs = [
    ("00_regioes_de_integracao_para.svg", make_bar_chart_svg(regioes_para, max_val=30.0, val_suffix="%", round_digits=2)),
    ("01_limites_e_unidades_conservacao.svg", make_bar_chart_svg(tema_01_items, max_val=100.0, val_suffix="%", round_digits=2)),
    ("02_gestao_e_infraestrutura.svg", make_bar_chart_svg(tema_02_items, max_val=60.0, val_suffix=" pts", round_digits=0)),
    ("03_biodiversidade_e_protecao_ambiental.svg", make_bar_chart_svg(tema_03_items, max_val=60.0, val_suffix=" reg", round_digits=0)),
    ("04_comunidades_e_uso_tradicional.svg", make_bar_chart_svg(tema_04_items, max_val=320.0, val_suffix=" un", round_digits=0)),
    ("05_geografia_e_hidrografia.svg", make_bar_chart_svg(tema_05_items, max_val=65.0, val_suffix=" feições", round_digits=0)),
]

for fname, content in all_svs:
    p = os.path.join(output_dir, fname)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated clean SVG: {p}")

print("\n--- All SVGs successfully created! ---")
