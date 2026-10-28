import os

output_dir = "paineis_tematicos_svg"
os.makedirs(output_dir, exist_ok=True)

FONT_FAMILY = "'Segoe UI Variable Small Semibold', 'Segoe UI Variable Small', 'Segoe UI Semibold', 'Segoe UI', Arial, sans-serif"

def svg_header(w=136.382, h=186.572):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">
  <defs>
    <style>
      text {{
        font-family: {FONT_FAMILY};
        font-weight: 600;
      }}
      .sec-title {{
        font-size: 3.2mm;
        fill: #212529;
        text-transform: uppercase;
        letter-spacing: 0.15mm;
      }}
      .th {{
        font-size: 2.3mm;
        fill: #ffffff;
      }}
      .td {{
        font-size: 2.3mm;
        fill: #212529;
      }}
      .td-num {{
        font-size: 2.3mm;
        fill: #212529;
        text-anchor: end;
      }}
      .kpi-val {{
        font-size: 4.8mm;
        text-anchor: middle;
      }}
      .kpi-lbl {{
        font-size: 1.9mm;
        fill: #495057;
        text-anchor: middle;
        text-transform: uppercase;
      }}
      .note-text {{
        font-size: 2.05mm;
        fill: #343a40;
        line-height: 1.3;
      }}
      .fn {{
        font-size: 1.8mm;
        fill: #6c757d;
      }}
    </style>
  </defs>
  <!-- Background -->
  <rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff" stroke="none" />
'''

def svg_footer():
    return '</svg>'

# ==============================================================================
# PAINEL 01: LIMITES E UNIDADES DE CONSERVAÇÃO
# ==============================================================================
def generate_panel_01():
    w, h = 136.382, 186.572
    out = [svg_header(w, h)]
    
    # 1. QUADRO DE INDICADORES TERRITORIAIS (Top: y = 2.0 to 22.0)
    card_w = (136.382 - 4.0 - 4.0) / 3.0 # ~42.79mm
    cards = [
        ("ÁREA TOTAL DO MOSAICO", "26.989 ha", "269,89 km² Protegidos", "#1b5e20", 2.0),
        ("REVIS TABULEIRO EMBAUBAL", "4.033 ha", "14,94% do Mosaico", "#d9480f", 2.0 + card_w + 2.0),
        ("RDS VITÓRIA DE SOUZEL", "22.956 ha", "85,06% do Mosaico", "#2b8a3e", 2.0 + (card_w + 2.0)*2)
    ]
    for lbl, val, sub, col, x in cards:
        out.append(f'''  <rect x="{x:.2f}" y="2.0" width="{card_w:.2f}" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="{x:.2f}" y="2.0" width="{card_w:.2f}" height="1.8" fill="{col}" stroke="none" rx="0" ry="0" />
  <text x="{x + card_w/2:.2f}" y="10.5" class="kpi-val" fill="{col}">{val}</text>
  <text x="{x + card_w/2:.2f}" y="15.2" class="kpi-lbl">{lbl}</text>
  <text x="{x + card_w/2:.2f}" y="18.8" class="kpi-lbl" fill="#868e96">{sub}</text>''')

    # 2. SÍNTESE JURÍDICO-INSTITUCIONAL (y = 25.0 to 65.0)
    out.append('''
  <!-- Seção 1: Síntese Normativa -->
  <text x="2.0" y="28.0" class="sec-title">SÍNTESE JURÍDICO-INSTITUCIONAL DAS UNIDADES</text>
  <line x1="2.0" y1="29.5" x2="134.38" y2="29.5" stroke="#333333" stroke-width="0.6" />
  
  <!-- Tabela Jurídica -->
  <rect x="2.0" y="31.0" width="132.38" height="5.5" fill="#333333" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="34.8" class="th">UNIDADE DE CONSERVAÇÃO</text>
  <text x="50.0" y="34.8" class="th">CATEGORIA (SNUC)</text>
  <text x="88.0" y="34.8" class="th">ATO DE CRIAÇÃO</text>
  <text x="132.0" y="34.8" class="th" text-anchor="end">ÁREA (ha)</text>
''')
    rows_uc = [
        ("REVIS Tabuleiro do Embaubal", "Proteção Integral (Refúgio)", "Decreto Estadual nº 1.567/2016", "4.033,40", "#ffffff"),
        ("RDS Vitória de Souzel", "Uso Sustentável (Reserva)", "Decreto Estadual nº 1.568/2016", "22.955,80", "#f8f9fa"),
        ("Mosaico Integrado (Total)", "Mosaico de UCs Estaduais", "Criação Simultânea (2016)", "26.989,20", "#e9ecef")
    ]
    cur_y = 36.5
    for name, cat, dec, area, bg in rows_uc:
        out.append(f'''  <rect x="2.0" y="{cur_y:.2f}" width="132.38" height="6.2" fill="{bg}" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="{cur_y + 4.2:.2f}" class="td"><b>{name}</b></text>
  <text x="50.0" y="{cur_y + 4.2:.2f}" class="td">{cat}</text>
  <text x="88.0" y="{cur_y + 4.2:.2f}" class="td">{dec}</text>
  <text x="132.0" y="{cur_y + 4.2:.2f}" class="td-num"><b>{area}</b></text>''')
        cur_y += 6.2

    # 3. COMPARATIVO TERRITORIAL EM BARRAS (y = 59.0 to 86.0)
    out.append('''
  <!-- Seção 2: Comparativo Territorial -->
  <text x="2.0" y="60.0" class="sec-title">PROPORÇÃO TERRITORIAL E ZONEAMENTO</text>
  <line x1="2.0" y1="61.5" x2="134.38" y2="61.5" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="63.5" width="132.38" height="23.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  
  <text x="5.0" y="68.0" class="td"><b>REVIS Tabuleiro do Embaubal:</b> 14,94% da área protegida (4.033,40 ha)</text>
  <rect x="5.0" y="69.5" width="19.78" height="4.5" fill="#d9480f" stroke="#333333" stroke-width="0.2" rx="0" ry="0" />
  <rect x="24.78" y="69.5" width="104.6" height="4.5" fill="#e9ecef" stroke="#ced4da" stroke-width="0.2" rx="0" ry="0" />
  
  <text x="5.0" y="79.0" class="td"><b>RDS Vitória de Souzel:</b> 85,06% da área protegida (22.955,80 ha)</text>
  <rect x="5.0" y="80.5" width="112.6" height="4.5" fill="#2b8a3e" stroke="#333333" stroke-width="0.2" rx="0" ry="0" />
  <rect x="117.6" y="80.5" width="11.78" height="4.5" fill="#e9ecef" stroke="#ced4da" stroke-width="0.2" rx="0" ry="0" />
''')

    # 4. TABELA DE DISTRIBUIÇÃO MUNICIPAL (y = 90.0 to 125.0)
    out.append('''
  <!-- Seção 3: Municípios -->
  <text x="2.0" y="91.5" class="sec-title">INSERÇÃO MUNICIPAL DAS UNIDADES</text>
  <line x1="2.0" y1="93.0" x2="134.38" y2="93.0" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="94.5" width="132.38" height="5.5" fill="#495057" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="98.3" class="th">MUNICÍPIO (PA)</text>
  <text x="45.0" y="98.3" class="th">REGIÃO DE INTEGRAÇÃO</text>
  <text x="92.0" y="98.3" class="th">UNIDADE INCIDENTE</text>
  <text x="132.0" y="98.3" class="th" text-anchor="end">SITUAÇÃO</text>

  <rect x="2.0" y="100.0" width="132.38" height="6.2" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="104.2" class="td"><b>Senador José Porfírio</b></text>
  <text x="45.0" y="104.2" class="td">Xingu</text>
  <text x="92.0" y="104.2" class="td">REVIS e RDS</text>
  <text x="132.0" y="104.2" class="td-num">Sede das Unidades</text>

  <rect x="2.0" y="106.2" width="132.38" height="6.2" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="110.4" class="td"><b>Porto de Moz</b></text>
  <text x="45.0" y="110.4" class="td">Xingu / Baixo Amazonas</text>
  <text x="92.0" y="110.4" class="td">RDS Vitória de Souzel</text>
  <text x="132.0" y="110.4" class="td-num">Porção Norte / Foz</text>
''')

    # 5. QUADRO DE DIRETRIZES DE GESTÃO E CONECTIVIDADE (y = 117.0 to 175.0)
    out.append('''
  <!-- Seção 4: Diretrizes de Gestão -->
  <text x="2.0" y="117.5" class="sec-title">DIRETRIZES TÉCNICAS E OBJETIVOS DE MANEJO</text>
  <line x1="2.0" y1="119.0" x2="134.38" y2="119.0" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="121.0" width="132.38" height="26.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="121.0" width="2.5" height="26.0" fill="#d9480f" stroke="none" rx="0" ry="0" />
  <text x="7.0" y="125.8" class="td" fill="#d9480f"><b>REVIS TABULEIRO DO EMBAUBAL (PROTEÇÃO INTEGRAL)</b></text>
  <text x="7.0" y="130.2" class="note-text">Tem como objetivo básico assegurar condições para a reprodução, descanso e alimentação</text>
  <text x="7.0" y="134.0" class="note-text">de quelônios aquáticos (destaque para a tartaruga-da-amazônia, tracajá e pitiú), bem como</text>
  <text x="7.0" y="137.8" class="note-text">a conservação de aves migratórias e da ictiofauna associada aos bancos de areia e ilhas fluviais.</text>
  <text x="7.0" y="141.6" class="note-text">É vedada a exploração direta de recursos naturais, permitindo-se apenas pesquisa e visitação.</text>

  <rect x="2.0" y="149.0" width="132.38" height="26.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="149.0" width="2.5" height="26.0" fill="#2b8a3e" stroke="none" rx="0" ry="0" />
  <text x="7.0" y="153.8" class="td" fill="#2b8a3e"><b>RDS VITÓRIA DE SOUZEL (USO SUSTENTÁVEL)</b></text>
  <text x="7.0" y="158.2" class="note-text">Objetiva valorizar, conservar e aperfeiçoar o conhecimento e as práticas de manejo tradicional</text>
  <text x="7.0" y="162.0" class="note-text">desenvolvidas pelas populações ribeirinhas residentes, garantindo a sustentabilidade da pesca</text>
  <text x="7.0" y="165.8" class="note-text">artesanal, do extrativismo vegetal e a permanência das famílias no território protegido.</text>
  <text x="7.0" y="169.6" class="note-text">A gestão é compartilhada via Conselho Gestor Deliberativo paritário com comunitários.</text>
''')

    # NOTAS DE RODAPÉ (y = 179.0 to 184.0)
    out.append('''
  <!-- Rodapé Técnico -->
  <line x1="2.0" y1="178.5" x2="134.38" y2="178.5" stroke="#ced4da" stroke-width="0.4" />
  <text x="2.0" y="181.8" class="fn">Fonte dos Dados: IDEFLOR-Bio / DGBIO (Decretos Estaduais 1.567 e 1.568 de 2016). Sistema Geodésico: SIRGAS 2000 UTM 22S.</text>
  <text x="2.0" y="184.6" class="fn">Elaboração Cartográfica: Equipe Técnica IDEFLOR-Bio / GRB (2026). Cartografia Temática Digital.</text>
''')
    out.append(svg_footer())
    return "\n".join(out)


# ==============================================================================
# PAINEL 02: GESTÃO TERRITORIAL E INFRAESTRUTURA
# ==============================================================================
def generate_panel_02():
    w, h = 136.382, 186.572
    out = [svg_header(w, h)]
    
    # 1. INDICADORES DE GESTÃO (y = 2.0 to 22.0)
    card_w = (136.382 - 4.0 - 4.0) / 3.0
    cards = [
        ("EQUIPAMENTOS OPERACIONAIS", "19", "Bases, Escolas e Apoio", "#0d47a1", 2.0),
        ("TRAJETOS E ACESSOS", "49", "Rotas Fluviais e Vias", "#5f3dc4", 2.0 + card_w + 2.0),
        ("ALERTAS E PRESSÕES", "07", "Focos de Fogo e Impacto", "#c92a2a", 2.0 + (card_w + 2.0)*2)
    ]
    for lbl, val, sub, col, x in cards:
        out.append(f'''  <rect x="{x:.2f}" y="2.0" width="{card_w:.2f}" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="{x:.2f}" y="2.0" width="{card_w:.2f}" height="1.8" fill="{col}" stroke="none" rx="0" ry="0" />
  <text x="{x + card_w/2:.2f}" y="10.5" class="kpi-val" fill="{col}">{val}</text>
  <text x="{x + card_w/2:.2f}" y="15.2" class="kpi-lbl">{lbl}</text>
  <text x="{x + card_w/2:.2f}" y="18.8" class="kpi-lbl" fill="#868e96">{sub}</text>''')

    # 2. INVENTÁRIO DISCRIMINADO DE INFRAESTRUTURA (y = 25.0 to 88.0)
    out.append('''
  <!-- Seção 1: Inventário de Equipamentos -->
  <text x="2.0" y="28.0" class="sec-title">INVENTÁRIO DE EQUIPAMENTOS PÚBLICOS E OPERACIONAIS</text>
  <line x1="2.0" y1="29.5" x2="134.38" y2="29.5" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="31.0" width="132.38" height="5.5" fill="#333333" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="34.8" class="th">EQUIPAMENTO / ESTRUTURA</text>
  <text x="55.0" y="34.8" class="th">LOCALIZAÇÃO / BASE</text>
  <text x="96.0" y="34.8" class="th">FUNÇÃO TÉCNICA</text>
  <text x="132.0" y="34.8" class="th" text-anchor="end">STATUS</text>
''')
    infra_rows = [
        ("Base Tabuleiro (IDEFLOR-Bio)", "Ilha Cipó Pitanga do Meio", "Fiscalização, apoio à pesquisa e alojamento", "Ativa", "#ffffff"),
        ("Antiga Base de Fiscalização IBDF", "Canal do Tabuleiro", "Ponto de observação e vigilância histórica", "Referência", "#f8f9fa"),
        ("Escola Sol Elarrant Canto", "Comunidade Rio Tamanduá", "Educação básica do campo / multisseriada", "Ativa", "#ffffff"),
        ("Barracão Igreja São Marcos", "Comunidade São Marcos", "Ponto de reunião comunitária e celebrações", "Comunitário", "#f8f9fa"),
        ("Farol de Canal", "Entrada do canal de navegação", "Sinalização e balizamento náutico noturno", "Ativo", "#ffffff"),
        ("Poço da Lama / Poço Porunas", "Área insular norte", "Captação de água e abastecimento de apoio", "Operacional", "#f8f9fa"),
        ("Campo de Futebol Comunitário", "Comunidade Carmelita", "Área de lazer e integração sociocultural", "Comunitário", "#ffffff"),
        ("Torre de Observação", "Ponto elevado estratégico", "Vigilância dos tabuleiros na época de desova", "Sazonal", "#f8f9fa")
    ]
    cur_y = 36.5
    for name, loc, func, status, bg in infra_rows:
        out.append(f'''  <rect x="2.0" y="{cur_y:.2f}" width="132.38" height="5.5" fill="{bg}" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="{cur_y + 3.8:.2f}" class="td"><b>{name}</b></text>
  <text x="55.0" y="{cur_y + 3.8:.2f}" class="td">{loc}</text>
  <text x="96.0" y="{cur_y + 3.8:.2f}" class="td">{func}</text>
  <text x="132.0" y="{cur_y + 3.8:.2f}" class="td-num"><b>{status}</b></text>''')
        cur_y += 5.5

    # 3. ROTAS DE PATRULHAMENTO E LOGÍSTICA FLUVIAL (y = 86.0 to 125.0)
    out.append('''
  <!-- Seção 2: Logística e Rotas -->
  <text x="2.0" y="87.0" class="sec-title">ROTAS DE PATRULHAMENTO FLUVIAL E ACESSOS TERRESTRES</text>
  <line x1="2.0" y1="88.5" x2="134.38" y2="88.5" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="90.0" width="132.38" height="31.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="90.0" width="2.5" height="31.0" fill="#5f3dc4" stroke="none" rx="0" ry="0" />
  <text x="7.0" y="94.5" class="td" fill="#5f3dc4"><b>MALHA FLUVIAL DE FISCALIZAÇÃO (49 PONTOS DE CONTROLE)</b></text>
  <text x="7.0" y="99.0" class="note-text">• <b>Canal Principal do Rio Xingu:</b> Patrulhamento com embarcação de grande porte e lanchas rápidas.</text>
  <text x="7.0" y="103.0" class="note-text">• <b>Furos Estratégicos de Patrulha:</b> Furo Bom Jardim, Furo Tapecurá, Furo da Camaleoa e Furo Juncal.</text>
  <text x="7.0" y="107.0" class="note-text">• <b>Pontos de Enseada e Igarapés:</b> Fiscalização com voadeiras de alumínio de baixo calado na cheia.</text>
  <text x="7.0" y="111.0" class="note-text">• <b>Porteiras e Acessos Terrestres:</b> Controle de vicinais off-road na margem direita (Barro Branco / Porfírio).</text>
  <text x="7.0" y="115.0" class="note-text">• <b>Tempo Médio de Deslocamento:</b> Base Tabuleiro até comunidades do sul: ~45 min; até Porto de Moz: ~2h30.</text>
''')

    # 4. MONITORAMENTO DE PRESSÕES E OCORRÊNCIAS (y = 127.0 to 175.0)
    out.append('''
  <!-- Seção 3: Alertas e Pressões -->
  <text x="2.0" y="128.5" class="sec-title">REGISTRO DE PRESSÕES E OCORRÊNCIAS AMBIENTAIS</text>
  <line x1="2.0" y1="130.0" x2="134.38" y2="130.0" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="132.0" width="132.38" height="5.5" fill="#495057" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="135.8" class="th">TIPO DE OCORRÊNCIA</text>
  <text x="50.0" y="135.8" class="th">REGISTRO TEMPORAL</text>
  <text x="90.0" y="135.8" class="th">IMPACTO CONSTATADO</text>
  <text x="132.0" y="135.8" class="th" text-anchor="end">AÇÃO</text>

  <rect x="2.0" y="137.5" width="132.38" height="6.2" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="141.7" class="td"><b>Incêndio Histórico de 1982</b></text>
  <text x="50.0" y="141.7" class="td">Registro histórico</text>
  <text x="90.0" y="141.7" class="td">Grande queima em vegetação de várzea</text>
  <text x="132.0" y="141.7" class="td-num">Regeneração</text>

  <rect x="2.0" y="143.7" width="132.38" height="6.2" fill="#fff5f5" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="147.9" class="td" fill="#c92a2a"><b>Queimada Recente (2024)</b></text>
  <text x="50.0" y="147.9" class="td">Fevereiro/2024</text>
  <text x="90.0" y="147.9" class="td">Cicatriz de fogo próxima ao Rio Cacau</text>
  <text x="132.0" y="147.9" class="td-num" fill="#c92a2a">Monitoramento</text>

  <rect x="2.0" y="149.9" width="132.38" height="6.2" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="154.1" class="td"><b>Presença de Búfalos</b></text>
  <text x="50.0" y="154.1" class="td">Contínuo (várzea)</text>
  <text x="90.0" y="154.1" class="td">Pisoteio de margens e compactação do solo</text>
  <text x="132.0" y="154.1" class="td-num">Notificação</text>

  <rect x="2.0" y="156.1" width="132.38" height="6.2" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="160.3" class="td"><b>Abertura Irregular de Canal</b></text>
  <text x="50.0" y="160.3" class="td">Demanda cadastrada</text>
  <text x="90.0" y="160.3" class="td">Risco de alteração da hidrodinâmica local</text>
  <text x="132.0" y="160.3" class="td-num">Indeferido</text>

  <rect x="2.0" y="164.0" width="132.38" height="11.5" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <text x="4.0" y="168.0" class="note-text"><b>Estratégia Integrada de Fiscalização:</b> Operações conjuntas com a Polícia Militar Ambiental (BPA) e</text>
  <text x="4.0" y="171.8" class="note-text">comunitários voluntários, com foco intensivo no período de postura e eclosão de quelônios (Setembro a Janeiro).</text>
''')

    # NOTAS DE RODAPÉ (y = 179.0 to 184.0)
    out.append('''
  <!-- Rodapé Técnico -->
  <line x1="2.0" y1="178.5" x2="134.38" y2="178.5" stroke="#ced4da" stroke-width="0.4" />
  <text x="2.0" y="181.8" class="fn">Fonte dos Dados: Levantamentos de Campo IDEFLOR-Bio (Equipes Kelly e Lorena, 2025-2026).</text>
  <text x="2.0" y="184.6" class="fn">Diretoria de Gestão e Monitoramento de Unidades de Conservação (DGBIO/GRB). Sistema SIRGAS 2000 UTM 22S.</text>
''')
    out.append(svg_footer())
    return "\n".join(out)


# ==============================================================================
# PAINEL 03: BIODIVERSIDADE E PROTEÇÃO AMBIENTAL
# ==============================================================================
def generate_panel_03():
    w, h = 136.382, 186.572
    out = [svg_header(w, h)]
    
    # 1. INDICADORES BIOLÓGICOS (y = 2.0 to 22.0)
    card_w = (136.382 - 4.0 - 4.0) / 3.0
    cards = [
        ("ÁREAS DE DESOVA", "22", "Tabuleiros Mapeados", "#007f5f", 2.0),
        ("FLORA E MATRIZES", "50", "Árvores Protegidas", "#2b9348", 2.0 + card_w + 2.0),
        ("ESPÉCIES-ALVO", "04", "Quelônios e Peixes", "#d48b00", 2.0 + (card_w + 2.0)*2)
    ]
    for lbl, val, sub, col, x in cards:
        out.append(f'''  <rect x="{x:.2f}" y="2.0" width="{card_w:.2f}" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="{x:.2f}" y="2.0" width="{card_w:.2f}" height="1.8" fill="{col}" stroke="none" rx="0" ry="0" />
  <text x="{x + card_w/2:.2f}" y="10.5" class="kpi-val" fill="{col}">{val}</text>
  <text x="{x + card_w/2:.2f}" y="15.2" class="kpi-lbl">{lbl}</text>
  <text x="{x + card_w/2:.2f}" y="18.8" class="kpi-lbl" fill="#868e96">{sub}</text>''')

    # 2. ESPÉCIES-ALVO DE QUELÔNIOS E ICTIOFAUNA (y = 25.0 to 76.0)
    out.append('''
  <!-- Seção 1: Espécies Protegidas -->
  <text x="2.0" y="28.0" class="sec-title">ESPÉCIES-ALVO DE QUELÔNIOS E ICTIOFAUNA PROTEGIDA</text>
  <line x1="2.0" y1="29.5" x2="134.38" y2="29.5" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="31.0" width="132.38" height="5.5" fill="#333333" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="34.8" class="th">ESPÉCIE / NOME CIENTÍFICO</text>
  <text x="56.0" y="34.8" class="th">HÁBITAT DE REPRODUÇÃO</text>
  <text x="96.0" y="34.8" class="th">STATUS E IMPORTÂNCIA</text>
  <text x="132.0" y="34.8" class="th" text-anchor="end">REGISTROS</text>
''')
    species = [
        ("Tartaruga-da-amazônia", "Podocnemis expansa", "Altos de praias fluviais e restingas arenosas", "Sítio reprodutivo crítico / Ameaçada", "Principal", "#ffffff"),
        ("Tracajá", "Podocnemis unifilis", "Bancos de areia, praias e margens de igarapés", "Vulnerável / Intensa postura local", "Abundante", "#f8f9fa"),
        ("Pitiú / Iaçá", "Podocnemis sextuberculata", "Bancos arenosos baixos e saibro fino", "Espécie protegida de menor porte", "Frequente", "#ffffff"),
        ("Curimatá", "Prochilodus nigricans", "Furos e canais de ligação com lagos de várzea", "Ictiofauna de piracema / Desova mapeada", "04 Pontos", "#f8f9fa"),
        ("Peixe-boi da Amazônia", "Trichechus inunguis", "Igarapé Japopaca e Lago Pitoa", "Mamífero aquático / Área de alimentação", "Refúgio", "#ffffff")
    ]
    cur_y = 36.5
    for comm, sci, hab, imp, reg, bg in species:
        out.append(f'''  <rect x="2.0" y="{cur_y:.2f}" width="132.38" height="7.2" fill="{bg}" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="{cur_y + 3.2:.2f}" class="td"><b>{comm}</b></text>
  <text x="4.0" y="{cur_y + 6.0:.2f}" class="fn" fill="#555555"><i>{sci}</i></text>
  <text x="56.0" y="{cur_y + 4.5:.2f}" class="td">{hab}</text>
  <text x="96.0" y="{cur_y + 4.5:.2f}" class="td">{imp}</text>
  <text x="132.0" y="{cur_y + 4.5:.2f}" class="td-num"><b>{reg}</b></text>''')
        cur_y += 7.2

    # 3. CRONOGRAMA FENOLÓGICO E HIDROLÓGICO (y = 78.0 to 125.0)
    out.append('''
  <!-- Seção 2: Calendário Reprodutivo -->
  <text x="2.0" y="79.0" class="sec-title">CALENDÁRIO REPRODUTIVO DOS QUELÔNIOS E REGIME DO RIO XINGU</text>
  <line x1="2.0" y1="80.5" x2="134.38" y2="80.5" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="82.0" width="132.38" height="38.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  
  <!-- Fases -->
  <rect x="4.0" y="84.0" width="40.0" height="34.0" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <rect x="4.0" y="84.0" width="40.0" height="2.0" fill="#d48b00" stroke="none" rx="0" ry="0" />
  <text x="6.0" y="89.0" class="td" fill="#d48b00"><b>1. VAZANTE / POSTURA</b></text>
  <text x="6.0" y="93.0" class="fn"><b>Período:</b> Agosto a Outubro</text>
  <text x="6.0" y="97.0" class="note-text">Exposição gradual dos tabuleiros</text>
  <text x="6.0" y="100.5" class="note-text">de areia. Subida coletiva das</text>
  <text x="6.0" y="104.0" class="note-text">fêmeas no período noturno para</text>
  <text x="6.0" y="107.5" class="note-text">escavação de covas e postura.</text>
  <text x="6.0" y="111.0" class="note-text">Período de máxima fiscalização.</text>

  <rect x="48.0" y="84.0" width="40.0" height="34.0" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <rect x="48.0" y="84.0" width="40.0" height="2.0" fill="#007f5f" stroke="none" rx="0" ry="0" />
  <text x="50.0" y="89.0" class="td" fill="#007f5f"><b>2. ECLOSÃO / RECRUTAMENTO</b></text>
  <text x="50.0" y="93.0" class="fn"><b>Período:</b> Novembro a Janeiro</text>
  <text x="50.0" y="97.0" class="note-text">Período de incubação de ~60 dias.</text>
  <text x="50.0" y="100.5" class="note-text">Nascimento em massa dos filhotes</text>
  <text x="50.0" y="104.0" class="note-text">e corrida sincronizada para o rio.</text>
  <text x="50.0" y="107.5" class="note-text">Ações de soltura monitorada pelo</text>
  <text x="50.0" y="111.0" class="note-text">IDEFLOR-Bio e voluntários.</text>

  <rect x="92.0" y="84.0" width="40.0" height="34.0" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <rect x="92.0" y="84.0" width="40.0" height="2.0" fill="#1864ab" stroke="none" rx="0" ry="0" />
  <text x="94.0" y="89.0" class="td" fill="#1864ab"><b>3. ENCHENTE / ALIMENTAÇÃO</b></text>
  <text x="94.0" y="93.0" class="fn"><b>Período:</b> Fevereiro a Julho</text>
  <text x="94.0" y="97.0" class="note-text">Subida das águas e inundação dos</text>
  <text x="94.0" y="100.5" class="note-text">tabuleiros. Dispersão das espécies</text>
  <text x="94.0" y="104.0" class="note-text">para florestas de igapó e várzea.</text>
  <text x="94.0" y="107.5" class="note-text">Fase de engorda e alimentação com</text>
  <text x="94.0" y="111.0" class="note-text">frutos e sementes florestais.</text>
''')

    # 4. PATRIMÔNIO FLORÍSTICO E ÁRVORES MATRIZES (y = 125.0 to 175.0)
    out.append('''
  <!-- Seção 3: Recursos Florísticos -->
  <text x="2.0" y="126.5" class="sec-title">INVENTÁRIO BOTÂNICO E ÁRVORES MATRIZES (50 PONTOS)</text>
  <line x1="2.0" y1="128.0" x2="134.38" y2="128.0" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="129.5" width="132.38" height="5.5" fill="#495057" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="133.3" class="th">ESPÉCIE BOTÂNICA</text>
  <text x="56.0" y="133.3" class="th">NOME CIENTÍFICO</text>
  <text x="96.0" y="133.3" class="th">TIPOLOGIA FLORESTAL</text>
  <text x="132.0" y="133.3" class="th" text-anchor="end">IMPORTÂNCIA</text>

  <rect x="2.0" y="135.0" width="132.38" height="6.2" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="139.2" class="td"><b>Seringueira com Lanho</b></text>
  <text x="56.0" y="139.2" class="td"><i>Hevea brasiliensis</i></text>
  <text x="96.0" y="139.2" class="td">Floresta de Várzea Alta</text>
  <text x="132.0" y="139.2" class="td-num">Extrativismo / Histórico</text>

  <rect x="2.0" y="141.2" width="132.38" height="6.2" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="145.4" class="td"><b>Jatobá</b></text>
  <text x="56.0" y="145.4" class="td"><i>Hymenaea courbaril</i></text>
  <text x="96.0" y="145.4" class="td">Mata de Terra Firme / Transição</text>
  <text x="132.0" y="145.4" class="td-num">Matriz / Alimento Fauna</text>

  <rect x="2.0" y="147.4" width="132.38" height="6.2" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="151.6" class="td"><b>Castanheira-do-Pará</b></text>
  <text x="56.0" y="151.6" class="td"><i>Bertholletia excelsa</i></text>
  <text x="96.0" y="151.6" class="td">Terra Firme Adjacente</text>
  <text x="132.0" y="151.6" class="td-num">Espécie Imune de Corte</text>

  <rect x="2.0" y="155.0" width="132.38" height="20.5" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <text x="4.0" y="159.5" class="note-text"><b>Conservação da Flora e Habitat:</b> O mosaico protege remanescentes de florestas aluviais densas periodicamente</text>
  <text x="4.0" y="163.5" class="note-text">inundadas que constituem fonte alimentar primária para os quelônios durante o período de águas altas.</text>
  <text x="4.0" y="167.5" class="note-text">A manutenção da cobertura florestal das ilhas (como a Ilha Goiabal e Mungubal) é vital para o controle térmico,</text>
  <text x="4.0" y="171.5" class="note-text">estabilização sedimentar das margens e redução da erosão dos bancos de areia reprodutivos.</text>
''')

    # NOTAS DE RODAPÉ (y = 179.0 to 184.0)
    out.append('''
  <!-- Rodapé Técnico -->
  <line x1="2.0" y1="178.5" x2="134.38" y2="178.5" stroke="#ced4da" stroke-width="0.4" />
  <text x="2.0" y="181.8" class="fn">Fonte dos Dados: Monitoramento de Quelônios e Botânica IDEFLOR-Bio (2025-2026). Datum SIRGAS 2000 UTM 22S.</text>
  <text x="2.0" y="184.6" class="fn">Refúgio de Vida Silvestre Tabuleiro do Embaubal e RDS Vitória de Souzel. Diretoria de Gestão da Biodiversidade (DGBIO).</text>
''')
    out.append(svg_footer())
    return "\n".join(out)


# ==============================================================================
# PAINEL 04: COMUNIDADES E USO TRADICIONAL
# ==============================================================================
def generate_panel_04():
    w, h = 136.382, 186.572
    out = [svg_header(w, h)]
    
    # 1. INDICADORES SOCIOESPACIAIS (y = 2.0 to 22.0)
    card_w = (136.382 - 4.0 - 4.0) / 3.0
    cards = [
        ("MORADIAS RIBEIRINHAS", "282", "Residências Cadastradas", "#e65100", 2.0),
        ("APOIO DE PESCA / RANCHOS", "89", "Estruturas de Pesca", "#00838f", 2.0 + card_w + 2.0),
        ("POPULAÇÃO PROTEGIDA", "100%", "RDS Vitória de Souzel", "#2e7d32", 2.0 + (card_w + 2.0)*2)
    ]
    for lbl, val, sub, col, x in cards:
        out.append(f'''  <rect x="{x:.2f}" y="2.0" width="{card_w:.2f}" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="{x:.2f}" y="2.0" width="{card_w:.2f}" height="1.8" fill="{col}" stroke="none" rx="0" ry="0" />
  <text x="{x + card_w/2:.2f}" y="10.5" class="kpi-val" fill="{col}">{val}</text>
  <text x="{x + card_w/2:.2f}" y="15.2" class="kpi-lbl">{lbl}</text>
  <text x="{x + card_w/2:.2f}" y="18.8" class="kpi-lbl" fill="#868e96">{sub}</text>''')

    # 2. CENSO E TIPOLOGIA DE OCUPAÇÃO (y = 25.0 to 76.0)
    out.append('''
  <!-- Seção 1: Censo de Ocupação -->
  <text x="2.0" y="28.0" class="sec-title">CENSO SOCIOESPACIAL E TIPOLOGIA DE OCUPAÇÃO ANTRÓPICA</text>
  <line x1="2.0" y1="29.5" x2="134.38" y2="29.5" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="31.0" width="132.38" height="5.5" fill="#333333" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="34.8" class="th">CATEGORIA DE ESTRUTURA</text>
  <text x="56.0" y="34.8" class="th">REGIME DE OCUPAÇÃO</text>
  <text x="96.0" y="34.8" class="th">DISTRIBUIÇÃO ESPACIAL</text>
  <text x="132.0" y="34.8" class="th" text-anchor="end">TOTAL</text>
''')
    socio_rows = [
        ("Residências Ribeirinhas Permanentes", "Permanente / Familiar", "Margens de rios, furos e restingas insulares", "282", "#ffffff"),
        ("Ranchos de Apoio de Pesca Ativos", "Sazonal / Período de Safra", "Próximo a pesqueiros, saídas de furos e canais", "89", "#f8f9fa"),
        ("Escolas Rurais Comunitárias", "Ano Letivo / Comunitário", "Polos concentradores (ex: Sol Elarrant Canto)", "Cadastradas", "#ffffff"),
        ("Igrejas e Centros Comunitários", "Eventos / Festividades", "Comunidade São Marcos, Carmelita e vilarejos", "Cadastradas", "#f8f9fa"),
        ("Total de Pontos de Uso Comunitário", "Socioeconomia Tradicional", "Território integral da RDS Vitória de Souzel", "371", "#e9ecef")
    ]
    cur_y = 36.5
    for cat, reg, dist, total, bg in socio_rows:
        out.append(f'''  <rect x="2.0" y="{cur_y:.2f}" width="132.38" height="6.2" fill="{bg}" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="{cur_y + 4.2:.2f}" class="td"><b>{cat}</b></text>
  <text x="56.0" y="{cur_y + 4.2:.2f}" class="td">{reg}</text>
  <text x="96.0" y="{cur_y + 4.2:.2f}" class="td">{dist}</text>
  <text x="132.0" y="{cur_y + 4.2:.2f}" class="td-num"><b>{total}</b></text>''')
        cur_y += 6.2

    # 3. PROPORÇÃO ENTRE MORADIAS E APOIOS DE PESCA (y = 70.0 to 102.0)
    out.append('''
  <!-- Seção 2: Proporção de Uso -->
  <text x="2.0" y="72.0" class="sec-title">ESTRUTURA DA OCUPAÇÃO RURAL E PESQUEIRA</text>
  <line x1="2.0" y1="73.5" x2="134.38" y2="73.5" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="75.5" width="132.38" height="25.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  
  <text x="5.0" y="80.5" class="td"><b>Residências Ribeirinhas (Habitação Permanente):</b> 76,01% (282 pontos)</text>
  <rect x="5.0" y="82.0" width="100.6" height="4.5" fill="#e65100" stroke="#333333" stroke-width="0.2" rx="0" ry="0" />
  <rect x="105.6" y="82.0" width="23.78" height="4.5" fill="#e9ecef" stroke="#ced4da" stroke-width="0.2" rx="0" ry="0" />

  <text x="5.0" y="91.5" class="td"><b>Ranchos de Pesca (Estruturas Sazonais de Apoio):</b> 23,99% (89 pontos)</text>
  <rect x="5.0" y="93.0" width="31.75" height="4.5" fill="#00838f" stroke="#333333" stroke-width="0.2" rx="0" ry="0" />
  <rect x="36.75" y="93.0" width="92.63" height="4.5" fill="#e9ecef" stroke="#ced4da" stroke-width="0.2" rx="0" ry="0" />
''')

    # 4. DINÂMICA DA PESCA ARTESANAL E ACORDOS COMUNITÁRIOS (y = 104.0 to 175.0)
    out.append('''
  <!-- Seção 3: Manejo e Pesca -->
  <text x="2.0" y="105.0" class="sec-title">DINÂMICA DA PESCA ARTESANAL E MANEJO PARTICIPATIVO</text>
  <line x1="2.0" y1="106.5" x2="134.38" y2="106.5" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="108.5" width="132.38" height="31.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="108.5" width="2.5" height="31.0" fill="#00838f" stroke="none" rx="0" ry="0" />
  <text x="7.0" y="113.0" class="td" fill="#00838f"><b>PRÁTICAS DE PESCA TRADICIONAL NA RDS VITÓRIA DE SOUZEL</b></text>
  <text x="7.0" y="117.5" class="note-text">• <b>Equipamentos Utilizados:</b> Malhadeiras com malhagem regulamentada, espinhéis, linhas de mão e tarrafas.</text>
  <text x="7.0" y="121.5" class="note-text">• <b>Principais Espécies de Consumo e Renda:</b> Curimatá, pacu, tucunaré, filhote/piraíba, pirarucu e aracu.</text>
  <text x="7.0" y="125.5" class="note-text">• <b>Função dos Ranchos de Pesca:</b> Pouso noturno, estaleiro para secagem de redes e salga/conservação do peixe.</text>
  <text x="7.0" y="129.5" class="note-text">• <b>Manejo de Quelônios:</b> O consumo tradicional é estritamente regulado; a caça predatória e o comércio são coibidos.</text>
  <text x="7.0" y="133.5" class="note-text">• <b>Pacto de Sustentabilidade:</b> A delimitação da RDS garantiu a posse pacífica e os direitos das famílias tradicionais.</text>

  <!-- Quadro de Gestão Participativa -->
  <rect x="2.0" y="142.5" width="132.38" height="33.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="142.5" width="2.5" height="33.0" fill="#e65100" stroke="none" rx="0" ry="0" />
  <text x="7.0" y="147.0" class="td" fill="#e65100"><b>CONSELHO GESTOR E VIGILÂNCIA COMUNITÁRIA</b></text>
  <text x="7.0" y="151.5" class="note-text">A gestão da RDS Vitória de Souzel fundamenta-se na participação social de ribeirinhos, pescadores e extrativistas.</text>
  <text x="7.0" y="155.5" class="note-text">Os comunitários atuam ativamente como monitores voluntários dos tabuleiros de postura do REVIS Tabuleiro do</text>
  <text x="7.0" y="159.5" class="note-text">Embaubal, consolidando uma aliança vital: a integridade biológica do refúgio depende diretamente da cooperação e do</text>
  <text x="7.0" y="163.5" class="note-text">engajamento das famílias ribeirinhas residentes no território contíguo da RDS.</text>
  <text x="7.0" y="167.5" class="note-text">O censo georreferenciado permite ao IDEFLOR-Bio planejar ações de saúde, abastecimento e fomento sustentável.</text>
''')

    # NOTAS DE RODAPÉ (y = 179.0 to 184.0)
    out.append('''
  <!-- Rodapé Técnico -->
  <line x1="2.0" y1="178.5" x2="134.38" y2="178.5" stroke="#ced4da" stroke-width="0.4" />
  <text x="2.0" y="181.8" class="fn">Fonte dos Dados: Cadastro Socioambiental e Cadastramento de Moradores (IDEFLOR-Bio, 2025-2026).</text>
  <text x="2.0" y="184.6" class="fn">Reserva de Desenvolvimento Sustentável Vitória de Souzel. Datum SIRGAS 2000 UTM 22S. Coordenadas Consolidadas.</text>
''')
    out.append(svg_footer())
    return "\n".join(out)


# ==============================================================================
# PAINEL 05: GEOGRAFIA E HIDROGRAFIA
# ==============================================================================
def generate_panel_05():
    w, h = 136.382, 186.572
    out = [svg_header(w, h)]
    
    # 1. INDICADORES HIDROMORFOLÓGICOS (y = 2.0 to 22.0)
    card_w = (136.382 - 4.0 - 4.0) / 3.0
    cards = [
        ("CORPOS HÍDRICOS", "134", "Rios, Furos e Igarapés", "#0077b6", 2.0),
        ("ILHAS E PRAIAS", "78", "Mosaico Insular e Areia", "#b07d4b", 2.0 + card_w + 2.0),
        ("MARCOS NÁUTICOS", "16", "Canais e Referências", "#495057", 2.0 + (card_w + 2.0)*2)
    ]
    for lbl, val, sub, col, x in cards:
        out.append(f'''  <rect x="{x:.2f}" y="2.0" width="{card_w:.2f}" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="{x:.2f}" y="2.0" width="{card_w:.2f}" height="1.8" fill="{col}" stroke="none" rx="0" ry="0" />
  <text x="{x + card_w/2:.2f}" y="10.5" class="kpi-val" fill="{col}">{val}</text>
  <text x="{x + card_w/2:.2f}" y="15.2" class="kpi-lbl">{lbl}</text>
  <text x="{x + card_w/2:.2f}" y="18.8" class="kpi-lbl" fill="#868e96">{sub}</text>''')

    # 2. HIERARQUIA DA REDE HIDROGRÁFICA (y = 25.0 to 76.0)
    out.append('''
  <!-- Seção 1: Rede Hidrográfica -->
  <text x="2.0" y="28.0" class="sec-title">HIERARQUIA E CLASSIFICAÇÃO DA REDE HIDROGRÁFICA</text>
  <line x1="2.0" y1="29.5" x2="134.38" y2="29.5" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="31.0" width="132.38" height="5.5" fill="#333333" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="34.8" class="th">TIPOLOGIA HÍDRICA</text>
  <text x="46.0" y="34.8" class="th">CARACTERÍSTICA DINÂMICA</text>
  <text x="96.0" y="34.8" class="th">EXEMPLOS PRINCIPAIS</text>
  <text x="132.0" y="34.8" class="th" text-anchor="end">PONTOS</text>
''')
    hydro_rows = [
        ("Rios Principais / Calha", "Vias navegáveis estruturantes perenes", "Rio Xingu, Rio Cacau, Rio Arapari, Rio Tamanduá", "27", "#ffffff"),
        ("Furos Fluviais (Atalhos)", "Canais que cortam ilhas e conectam braços", "Furo Bom Jardim, Camaleoa, Tapecurá, Goiabal", "33", "#f8f9fa"),
        ("Igarapés de Várzea e Igapó", "Drenagem interna e florestal de médio porte", "Igarapé Atuca, Japopaca, Pitoa, Santa Tereza", "28", "#ffffff"),
        ("Lagos e Ressacos de Várzea", "Corpos lentos de alimentação e refúgio", "Lago Aramamba, Lago Pitoa, Lago do Palhau", "07", "#f8f9fa"),
        ("Poços Artesianos e Cacimbas", "Captação de água doce subterrânea", "Poço da Lama, Poço dos Porunas", "03", "#ffffff")
    ]
    cur_y = 36.5
    for cat, dyn, ex, count, bg in hydro_rows:
        out.append(f'''  <rect x="2.0" y="{cur_y:.2f}" width="132.38" height="6.2" fill="{bg}" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="{cur_y + 4.2:.2f}" class="td"><b>{cat}</b></text>
  <text x="46.0" y="{cur_y + 4.2:.2f}" class="td">{dyn}</text>
  <text x="96.0" y="{cur_y + 4.2:.2f}" class="td">{ex}</text>
  <text x="132.0" y="{cur_y + 4.2:.2f}" class="td-num"><b>{count}</b></text>''')
        cur_y += 6.2

    # 3. MOSAICO INSULAR E PRAIAS FLUVIAIS (y = 70.0 to 120.0)
    out.append('''
  <!-- Seção 2: Morfologia Insular -->
  <text x="2.0" y="72.0" class="sec-title">MORFOLOGIA INSULAR E PRAIAS FLUVIAIS (78 PONTOS)</text>
  <line x1="2.0" y1="73.5" x2="134.38" y2="73.5" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="75.0" width="132.38" height="5.5" fill="#495057" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="78.8" class="th">FEIÇÃO MORFOLÓGICA</text>
  <text x="50.0" y="78.8" class="th">PAPEL ECOLÓGICO E NAVEGAÇÃO</text>
  <text x="96.0" y="78.8" class="th">PRINCIPAIS REGISTROS</text>
  <text x="132.0" y="78.8" class="th" text-anchor="end">STATUS</text>

  <rect x="2.0" y="80.5" width="132.38" height="6.2" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="84.7" class="td"><b>Grandes Ilhas Aluviais</b></text>
  <text x="50.0" y="84.7" class="td">Ilhas estáveis com matas densas de várzea</text>
  <text x="96.0" y="84.7" class="td">Ilha Embaubal, Abaeté, Cipó Pitanga</text>
  <text x="132.0" y="84.7" class="td-num">Perene</text>

  <rect x="2.0" y="86.7" width="132.38" height="6.2" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="90.9" class="td"><b>Ilhas Menores e Ilhotas</b></text>
  <text x="50.0" y="90.9" class="td">Refúgio de fauna e divisórias de canais</text>
  <text x="96.0" y="90.9" class="td">Ilha da Preguiça, Goiabal, Mungubal</text>
  <text x="132.0" y="90.9" class="td-num">Perene</text>

  <rect x="2.0" y="92.9" width="132.38" height="6.2" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="97.1" class="td"><b>Praias Fluviais e Pontas</b></text>
  <text x="50.0" y="97.1" class="td">Sedimentação de areia grossa e média</text>
  <text x="96.0" y="97.1" class="td">Praia do Gigi, Ponta do Navio, Paneminha</text>
  <text x="132.0" y="97.1" class="td-num">Sazonal</text>

  <rect x="2.0" y="99.1" width="132.38" height="6.2" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="103.3" class="td"><b>Bancos de Areia Emersos</b></text>
  <text x="50.0" y="103.3" class="td">Áreas de nidificação de quelônios e aves</text>
  <text x="96.0" y="103.3" class="td">Bancos da Boca das Ilhas e Meio do Rio</text>
  <text x="132.0" y="103.3" class="td-num">Sazonal</text>
''')

    # 4. PULSO DE INUNDAÇÃO E DINÂMICA SEDIMENTAR (y = 108.0 to 175.0)
    out.append('''
  <!-- Seção 3: Pulso de Inundação -->
  <text x="2.0" y="109.5" class="sec-title">PULSO DE INUNDAÇÃO DO BAIXO XINGU E DINÂMICA SEDIMENTAR</text>
  <line x1="2.0" y1="111.0" x2="134.38" y2="111.0" stroke="#333333" stroke-width="0.6" />

  <rect x="2.0" y="113.0" width="132.38" height="30.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="113.0" width="2.5" height="30.0" fill="#0077b6" stroke="none" rx="0" ry="0" />
  <text x="7.0" y="117.5" class="td" fill="#0077b6"><b>VARIAÇÃO HIDROMÉTRICA SAZONAL (4 A 6 METROS DE AMPLITUDE)</b></text>
  <text x="7.0" y="122.0" class="note-text">• <b>Estiagem (Agosto - Novembro):</b> Queda acentuada da lâmina d'água; formação dos extensos tabuleiros de areia</text>
  <text x="7.0" y="125.8" class="note-text">  e fechamento de furos rasos, concentrando a navegação nos canais de maior profundidade balizados por faróis.</text>
  <text x="7.0" y="129.6" class="note-text">• <b>Cheia (Fevereiro - Junho):</b> Elevação do nível das águas, afogamento completo dos bancos arenosos e abertura de</text>
  <text x="7.0" y="133.4" class="note-text">  todos os furos navegáveis, conectando o rio principal aos lagos de várzea internos e florestas de igapó.</text>
  <text x="7.0" y="137.2" class="note-text">• <b>Morfodinâmica dos Sedimentos:</b> O transporte de sedimentos de fundo do Xingu reconstitui as praias anualmente.</text>

  <!-- Quadro de Marcos Náuticos -->
  <rect x="2.0" y="146.0" width="132.38" height="29.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="146.0" width="2.5" height="29.0" fill="#b07d4b" stroke="none" rx="0" ry="0" />
  <text x="7.0" y="150.5" class="td" fill="#b07d4b"><b>NAVEGABILIDADE E MARCOS NÁUTICOS DE REFERÊNCIA</b></text>
  <text x="7.0" y="155.0" class="note-text">O labirinto de ilhas e bancos de areia torna a navegação no Baixo Xingu altamente dependente do conhecimento</text>
  <text x="7.0" y="159.0" class="note-text">tradicional e dos marcos cartográficos levantados: a boca de entrada dos furos (como a Boca do Juncal e Furo da Camaleoa),</text>
  <text x="7.0" y="163.0" class="note-text">as passagens de canais (Canal do Sacrifício) e o Farol de Canal são pontos críticos para a segurança das embarcações</text>
  <text x="7.0" y="167.0" class="note-text">da fiscalização do IDEFLOR-Bio e das embarcações mistas de passageiros e pescadores regionais.</text>
''')

    # NOTAS DE RODAPÉ (y = 179.0 to 184.0)
    out.append('''
  <!-- Rodapé Técnico -->
  <line x1="2.0" y1="178.5" x2="134.38" y2="178.5" stroke="#ced4da" stroke-width="0.4" />
  <text x="2.0" y="181.8" class="fn">Fonte dos Dados: Cartografia Hidrográfica e Morfológica IDEFLOR-Bio (2025-2026). Datum SIRGAS 2000 UTM 22S.</text>
  <text x="2.0" y="184.6" class="fn">Mosaico REVIS Tabuleiro do Embaubal e RDS Vitória de Souzel. Bacia do Rio Xingu, Pará.</text>
''')
    out.append(svg_footer())
    return "\n".join(out)


# Save all files
files = [
    ("01_limites_e_unidades_conservacao.svg", generate_panel_01()),
    ("02_gestao_e_infraestrutura.svg", generate_panel_02()),
    ("03_biodiversidade_e_protecao_ambiental.svg", generate_panel_03()),
    ("04_comunidades_e_uso_tradicional.svg", generate_panel_04()),
    ("05_geografia_e_hidrografia.svg", generate_panel_05())
]

for fname, content in files:
    path = os.path.join(output_dir, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated: {path} ({len(content)} bytes)")

print("\nAll 5 Technical SVG Panels Generated Successfully!")
