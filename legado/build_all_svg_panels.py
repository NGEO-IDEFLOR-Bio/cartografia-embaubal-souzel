import os
import sys

output_dir = "paineis_tematicos_svg"
os.makedirs(output_dir, exist_ok=True)

FONT = "Segoe UI Variable Small Semibold, Segoe UI Semibold, Segoe UI, Arial"

def get_header(w=136.382, h=186.572):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff" stroke="none" />
'''

def get_footer():
    return '</svg>'

# ==============================================================================
# PAINEL 01: LIMITES E UCs
# ==============================================================================
def gen_panel_01():
    w, h = 136.382, 186.572
    svg = [get_header(w, h)]
    
    # 1. INDICADORES
    svg.append(f'''  <!-- 1. INDICADORES TERRITORIAIS -->
  <rect x="2.0" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="2.0" width="42.79" height="1.8" fill="#1b5e20" stroke="none" rx="0" ry="0" />
  <text x="23.4" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#1b5e20" text-anchor="middle">26.989 ha</text>
  <text x="23.4" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">ÁREA DO MOSAICO</text>
  <text x="23.4" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">269,89 km² Protegidos</text>

  <rect x="46.79" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="46.79" y="2.0" width="42.79" height="1.8" fill="#d9480f" stroke="none" rx="0" ry="0" />
  <text x="68.19" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#d9480f" text-anchor="middle">4.033 ha</text>
  <text x="68.19" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">REVIS EMBAUBAL</text>
  <text x="68.19" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">14,94% do Mosaico</text>

  <rect x="91.58" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="91.58" y="2.0" width="42.79" height="1.8" fill="#2b8a3e" stroke="none" rx="0" ry="0" />
  <text x="112.98" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#2b8a3e" text-anchor="middle">22.956 ha</text>
  <text x="112.98" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">RDS V. DE SOUZEL</text>
  <text x="112.98" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">85,06% do Mosaico</text>

  <!-- 2. SÍNTESE JURÍDICO-INSTITUCIONAL -->
  <text x="2.0" y="28.0" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">SÍNTESE JURÍDICO-INSTITUCIONAL DAS UNIDADES</text>
  <line x1="2.0" y1="29.5" x2="134.38" y2="29.5" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="31.0" width="132.38" height="5.0" fill="#333333" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">UNIDADE DE CONSERVAÇÃO</text>
  <text x="52.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">CATEGORIA (SNUC)</text>
  <text x="88.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">ATO DE CRIAÇÃO</text>
  <text x="132.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff" text-anchor="end">ÁREA (ha)</text>

  <rect x="2.0" y="36.0" width="132.38" height="5.5" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="39.8" font-family="{FONT}" font-size="2.1" font-weight="600" fill="#d9480f">REVIS Tabuleiro do Embaubal</text>
  <text x="52.0" y="39.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Proteção Integral (Refúgio)</text>
  <text x="88.0" y="39.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Decreto Est. nº 1.567/2016</text>
  <text x="132.0" y="39.8" font-family="{FONT}" font-size="2.1" font-weight="600" fill="#212529" text-anchor="end">4.033,40</text>

  <rect x="2.0" y="41.5" width="132.38" height="5.5" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="45.3" font-family="{FONT}" font-size="2.1" font-weight="600" fill="#2b8a3e">RDS Vitória de Souzel</text>
  <text x="52.0" y="45.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Uso Sustentável (Reserva)</text>
  <text x="88.0" y="45.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Decreto Est. nº 1.568/2016</text>
  <text x="132.0" y="45.3" font-family="{FONT}" font-size="2.1" font-weight="600" fill="#212529" text-anchor="end">22.955,80</text>

  <rect x="2.0" y="47.0" width="132.38" height="5.5" fill="#e9ecef" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="50.8" font-family="{FONT}" font-size="2.1" font-weight="600" fill="#212529">Mosaico Integrado (Total)</text>
  <text x="52.0" y="50.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Mosaico de UCs Estaduais</text>
  <text x="88.0" y="50.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Criação Simultânea (2016)</text>
  <text x="132.0" y="50.8" font-family="{FONT}" font-size="2.1" font-weight="600" fill="#212529" text-anchor="end">26.989,20</text>

  <!-- 3. PROPORÇÃO TERRITORIAL -->
  <text x="2.0" y="57.5" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">PROPORÇÃO TERRITORIAL DAS UNIDADES</text>
  <line x1="2.0" y1="59.0" x2="134.38" y2="59.0" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="60.5" width="132.38" height="21.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <text x="5.0" y="64.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">REVIS Tabuleiro do Embaubal: 14,94% (4.033,40 ha)</text>
  <rect x="5.0" y="66.0" width="18.5" height="4.0" fill="#d9480f" stroke="#333333" stroke-width="0.2" rx="0" ry="0" />
  <rect x="23.5" y="66.0" width="105.5" height="4.0" fill="#e9ecef" stroke="#ced4da" stroke-width="0.2" rx="0" ry="0" />

  <text x="5.0" y="74.2" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">RDS Vitória de Souzel: 85,06% (22.955,80 ha)</text>
  <rect x="5.0" y="75.5" width="105.5" height="4.0" fill="#2b8a3e" stroke="#333333" stroke-width="0.2" rx="0" ry="0" />
  <rect x="110.5" y="75.5" width="18.5" height="4.0" fill="#e9ecef" stroke="#ced4da" stroke-width="0.2" rx="0" ry="0" />

  <!-- 4. INSERÇÃO MUNICIPAL -->
  <text x="2.0" y="86.0" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">INSERÇÃO MUNICIPAL DAS UNIDADES</text>
  <line x1="2.0" y1="87.5" x2="134.38" y2="87.5" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="89.0" width="132.38" height="5.0" fill="#495057" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="92.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">MUNICÍPIO (PA)</text>
  <text x="46.0" y="92.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">REGIÃO DE INTEGRAÇÃO</text>
  <text x="90.0" y="92.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">UNIDADE INCIDENTE</text>
  <text x="132.0" y="92.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff" text-anchor="end">SITUAÇÃO</text>

  <rect x="2.0" y="94.0" width="132.38" height="5.5" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="97.8" font-family="{FONT}" font-size="2.1" font-weight="600" fill="#212529">Senador José Porfírio</text>
  <text x="46.0" y="97.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Xingu</text>
  <text x="90.0" y="97.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">REVIS e RDS</text>
  <text x="132.0" y="97.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">Sede das UCs</text>

  <rect x="2.0" y="99.5" width="132.38" height="5.5" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="103.3" font-family="{FONT}" font-size="2.1" font-weight="600" fill="#212529">Porto de Moz</text>
  <text x="46.0" y="103.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Xingu / Baixo Amazonas</text>
  <text x="90.0" y="103.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">RDS Vitória de Souzel</text>
  <text x="132.0" y="103.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">Porção Norte / Foz</text>

  <!-- 5. DIRETRIZES TÉCNICAS E DE MANEJO -->
  <text x="2.0" y="110.0" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">DIRETRIZES TÉCNICAS E OBJETIVOS DE MANEJO</text>
  <line x1="2.0" y1="111.5" x2="134.38" y2="111.5" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="113.5" width="132.38" height="28.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="113.5" width="2.5" height="28.0" fill="#d9480f" stroke="none" rx="0" ry="0" />
  <text x="6.5" y="118.0" font-family="{FONT}" font-size="2.2" font-weight="600" fill="#d9480f">REVIS TABULEIRO DO EMBAUBAL (PROTEÇÃO INTEGRAL)</text>
  <text x="6.5" y="122.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• Objetivo precípuo: Proteger os ambientes naturais de reprodução de quelônios aquáticos</text>
  <text x="6.5" y="126.0" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">  (Tartaruga-da-amazônia, Tracajá e Pitiú) e conservar a ictiofauna e aves migratórias.</text>
  <text x="6.5" y="129.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• Regime restritivo: Não é permitida a exploração direta ou ocupação humana; admissível</text>
  <text x="6.5" y="133.0" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">  apenas a pesquisa científica autorizada e ações de educação ambiental / fiscalização.</text>
  <text x="6.5" y="136.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• Assegura a integridade física dos bancos de areia durante todo o período reprodutivo.</text>

  <rect x="2.0" y="144.0" width="132.38" height="28.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="144.0" width="2.5" height="28.0" fill="#2b8a3e" stroke="none" rx="0" ry="0" />
  <text x="6.5" y="148.5" font-family="{FONT}" font-size="2.2" font-weight="600" fill="#2b8a3e">RDS VITÓRIA DE SOUZEL (USO SUSTENTÁVEL)</text>
  <text x="6.5" y="153.0" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• Objetivo básico: Valorizar e aperfeiçoar o manejo tradicional dos recursos naturais pelas</text>
  <text x="6.5" y="156.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">  populações ribeirinhas residentes, conciliando conservação e desenvolvimento social.</text>
  <text x="6.5" y="160.0" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• Ordenamento: Regulamenta a pesca artesanal de subsistência e o extrativismo vegetal.</text>
  <text x="6.5" y="163.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• Participação social: Gestão deliberativa compartilhada via Conselho Gestor paritário.</text>
  <text x="6.5" y="167.0" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• A permanência dos ribeirinhos funciona como escudo territorial e proteção contígua ao REVIS.</text>

  <!-- RODAPÉ TÉCNICO -->
  <line x1="2.0" y1="176.0" x2="134.38" y2="176.0" stroke="#ced4da" stroke-width="0.3" />
  <text x="2.0" y="180.0" font-family="{FONT}" font-size="1.75" font-weight="600" fill="#6c757d">Fonte: IDEFLOR-Bio / DGBIO (Decretos Estaduais 1.567 e 1.568 de 2016). Sistema Geodésico: SIRGAS 2000 UTM 22S.</text>
  <text x="2.0" y="183.2" font-family="{FONT}" font-size="1.75" font-weight="600" fill="#6c757d">Elaboração Cartográfica: Equipe Técnica IDEFLOR-Bio / GRB (2026). Cartografia Temática Digital A1.</text>''')
    svg.append(get_footer())
    return "\n".join(svg)


# ==============================================================================
# PAINEL 02: GESTÃO E INFRAESTRUTURA
# ==============================================================================
def gen_panel_02():
    w, h = 136.382, 186.572
    svg = [get_header(w, h)]
    
    # 1. INDICADORES
    svg.append(f'''  <!-- 1. INDICADORES -->
  <rect x="2.0" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="2.0" width="42.79" height="1.8" fill="#0d47a1" stroke="none" rx="0" ry="0" />
  <text x="23.4" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#0d47a1" text-anchor="middle">19</text>
  <text x="23.4" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">EQUIPAMENTOS PÚBLICOS</text>
  <text x="23.4" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">Bases, Escolas e Apoio</text>

  <rect x="46.79" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="46.79" y="2.0" width="42.79" height="1.8" fill="#5f3dc4" stroke="none" rx="0" ry="0" />
  <text x="68.19" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#5f3dc4" text-anchor="middle">49</text>
  <text x="68.19" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">TRAJETOS E ACESSOS</text>
  <text x="68.19" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">Rotas Fluviais e Vias</text>

  <rect x="91.58" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="91.58" y="2.0" width="42.79" height="1.8" fill="#c92a2a" stroke="none" rx="0" ry="0" />
  <text x="112.98" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#c92a2a" text-anchor="middle">07</text>
  <text x="112.98" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">ALERTAS E PRESSÕES</text>
  <text x="112.98" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">Queimadas e Búfalos</text>

  <!-- 2. INVENTÁRIO DISCRIMINADO -->
  <text x="2.0" y="28.0" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">INVENTÁRIO DE EQUIPAMENTOS PÚBLICOS E OPERACIONAIS</text>
  <line x1="2.0" y1="29.5" x2="134.38" y2="29.5" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="31.0" width="132.38" height="5.0" fill="#333333" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">EQUIPAMENTO / ESTRUTURA</text>
  <text x="56.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">LOCALIZAÇÃO / BASE</text>
  <text x="96.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">FUNÇÃO TÉCNICA</text>
  <text x="132.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff" text-anchor="end">STATUS</text>
''')
    rows_infra = [
        ("Base Tabuleiro (IDEFLOR-Bio)", "Ilha Cipó Pitanga do Meio", "Fiscalização, apoio à pesquisa e alojamento", "Ativa", "#ffffff"),
        ("Antiga Base de Fiscalização IBDF", "Canal do Tabuleiro", "Ponto de observação e vigilância histórica", "Referência", "#f8f9fa"),
        ("Escola Sol Elarrant Canto", "Comunidade Rio Tamanduá", "Educação básica do campo / multisseriada", "Ativa", "#ffffff"),
        ("Barracão Igreja São Marcos", "Comunidade São Marcos", "Ponto de reunião comunitária e celebrações", "Comunitário", "#f8f9fa"),
        ("Farol de Canal", "Entrada do canal navegável", "Sinalização e balizamento náutico noturno", "Ativo", "#ffffff"),
        ("Poço da Lama / Poço Porunas", "Área insular norte", "Captação de água doce subterrânea", "Operacional", "#f8f9fa"),
        ("Campo de Futebol Comunitário", "Comunidade Carmelita", "Área de lazer e integração sociocultural", "Comunitário", "#ffffff"),
        ("Torre de Observação", "Ponto elevado estratégico", "Vigilância dos tabuleiros na desova", "Sazonal", "#f8f9fa")
    ]
    cur_y = 36.0
    for name, loc, func, status, bg in rows_infra:
        svg.append(f'''  <rect x="2.0" y="{cur_y:.2f}" width="132.38" height="5.2" fill="{bg}" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="{cur_y + 3.6:.2f}" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">{name}</text>
  <text x="56.0" y="{cur_y + 3.6:.2f}" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">{loc}</text>
  <text x="96.0" y="{cur_y + 3.6:.2f}" font-family="{FONT}" font-size="1.9" font-weight="600" fill="#495057">{func}</text>
  <text x="132.0" y="{cur_y + 3.6:.2f}" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">{status}</text>''')
        cur_y += 5.2

    # 3. MALHA FLUVIAL DE PATRULHAMENTO
    svg.append(f'''
  <!-- 3. MALHA FLUVIAL DE FISCALIZAÇÃO -->
  <text x="2.0" y="81.0" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">MALHA FLUVIAL DE PATRULHAMENTO E LOGÍSTICA</text>
  <line x1="2.0" y1="82.5" x2="134.38" y2="82.5" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="84.0" width="132.38" height="34.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="84.0" width="2.5" height="34.0" fill="#5f3dc4" stroke="none" rx="0" ry="0" />
  <text x="6.5" y="88.5" font-family="{FONT}" font-size="2.2" font-weight="600" fill="#5f3dc4">ROTAS DE FISCALIZAÇÃO E PONTOS DE CONTROLE (49 PONTOS)</text>
  <text x="6.5" y="93.0" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Canal Principal do Rio Xingu:</b> Patrulhamento hidroviário de médio e longo curso.</text>
  <text x="6.5" y="96.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Furos Estratégicos:</b> Rastreio no Furo Bom Jardim, Furo Tapecurá, Furo da Camaleoa e Furo Juncal.</text>
  <text x="6.5" y="100.6" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Igarapés de Várzea:</b> Patrulhas de curto alcance com voadeiras de alumínio e motor de popa.</text>
  <text x="6.5" y="104.4" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Vicinais e Porteiras:</b> Pontos de controle terrestre no limite leste (acesso à estrada do Barbicha/Porfírio).</text>
  <text x="6.5" y="108.2" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Tempos Operacionais:</b> Base Tabuleiro até comunidades do sul: ~45 min; até Porto de Moz: ~2h30.</text>
  <text x="6.5" y="112.0" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Infraestrutura de Apoio:</b> Presença de pontos de abastecimento e fonia/rádio nas bases estaduais.</text>

  <!-- 4. ALERTAS E OCORRÊNCIAS AMBIENTAIS -->
  <text x="2.0" y="122.0" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">REGISTRO DE PRESSÕES E OCORRÊNCIAS AMBIENTAIS</text>
  <line x1="2.0" y1="123.5" x2="134.38" y2="123.5" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="125.0" width="132.38" height="5.0" fill="#495057" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="128.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">TIPO DE OCORRÊNCIA</text>
  <text x="50.0" y="128.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">REGISTRO / ANO</text>
  <text x="90.0" y="128.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">IMPACTO CONSTATADO</text>
  <text x="132.0" y="128.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff" text-anchor="end">AÇÃO</text>

  <rect x="2.0" y="130.0" width="132.38" height="5.5" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="133.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Incêndio Histórico (1982)</text>
  <text x="50.0" y="133.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Registro histórico</text>
  <text x="90.0" y="133.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Grande queima em vegetação de várzea</text>
  <text x="132.0" y="133.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">Regeneração</text>

  <rect x="2.0" y="135.5" width="132.38" height="5.5" fill="#fff5f5" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="139.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#c92a2a">Queimada Recente (2024)</text>
  <text x="50.0" y="139.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Ano 2024</text>
  <text x="90.0" y="139.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Cicatriz de fogo próxima ao Rio Cacau</text>
  <text x="132.0" y="139.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#c92a2a" text-anchor="end">Monitoramento</text>

  <rect x="2.0" y="141.0" width="132.38" height="5.5" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="144.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Presença de Búfalos</text>
  <text x="50.0" y="144.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Contínuo (várzea)</text>
  <text x="90.0" y="144.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Pisoteio de margens e compactação</text>
  <text x="132.0" y="144.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">Notificação</text>

  <rect x="2.0" y="146.5" width="132.38" height="5.5" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="150.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Demanda Abertura de Canal</text>
  <text x="50.0" y="150.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Requerimento local</text>
  <text x="90.0" y="150.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Risco de alteração hidrodinâmica</text>
  <text x="132.0" y="150.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">Indeferido</text>

  <rect x="2.0" y="154.0" width="132.38" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <text x="4.0" y="158.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40"><b>Estratégia Integrada de Fiscalização:</b> O monitoramento das unidades opera de forma contínua durante todo o</text>
  <text x="4.0" y="162.2" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">ano, com reforço de efetivo de agentes ambientais no período crítico da reprodução de quelônios (Setembro a Janeiro).</text>
  <text x="4.0" y="166.0" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">As rotas fluviais mapeadas garantem resposta rápida a invasões e proteção das praias de nidificação.</text>
  <text x="4.0" y="169.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">A vigilância é realizada em conjunto com a Polícia Militar Ambiental (BPA) e monitores comunitários voluntários.</text>

  <!-- RODAPÉ TÉCNICO -->
  <line x1="2.0" y1="176.0" x2="134.38" y2="176.0" stroke="#ced4da" stroke-width="0.3" />
  <text x="2.0" y="180.0" font-family="{FONT}" font-size="1.75" font-weight="600" fill="#6c757d">Fonte: Levantamento de Campo e Fiscalização IDEFLOR-Bio (2025-2026). Sistema Geodésico: SIRGAS 2000 UTM 22S.</text>
  <text x="2.0" y="183.2" font-family="{FONT}" font-size="1.75" font-weight="600" fill="#6c757d">Diretoria de Gestão e Monitoramento de Unidades de Conservação (DGBIO/GRB). Cartografia Temática A1.</text>''')
    svg.append(get_footer())
    return "\n".join(svg)


# ==============================================================================
# PAINEL 03: BIODIVERSIDADE E PROTEÇÃO AMBIENTAL
# ==============================================================================
def gen_panel_03():
    w, h = 136.382, 186.572
    svg = [get_header(w, h)]
    
    # 1. INDICADORES
    svg.append(f'''  <!-- 1. INDICADORES BIOLÓGICOS -->
  <rect x="2.0" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="2.0" width="42.79" height="1.8" fill="#007f5f" stroke="none" rx="0" ry="0" />
  <text x="23.4" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#007f5f" text-anchor="middle">22</text>
  <text x="23.4" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">ÁREAS DE DESOVA</text>
  <text x="23.4" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">Tabuleiros Mapeados</text>

  <rect x="46.79" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="46.79" y="2.0" width="42.79" height="1.8" fill="#2b9348" stroke="none" rx="0" ry="0" />
  <text x="68.19" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#2b9348" text-anchor="middle">50</text>
  <text x="68.19" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">REGISTROS DE FLORA</text>
  <text x="68.19" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">Árvores Matrizes</text>

  <rect x="91.58" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="91.58" y="2.0" width="42.79" height="1.8" fill="#d48b00" stroke="none" rx="0" ry="0" />
  <text x="112.98" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#d48b00" text-anchor="middle">04</text>
  <text x="112.98" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">ESPÉCIES-ALVO</text>
  <text x="112.98" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">Quelônios e Peixes</text>

  <!-- 2. ESPÉCIES-ALVO -->
  <text x="2.0" y="28.0" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">ESPÉCIES-ALVO DE QUELÔNIOS E ICTIOFAUNA PROTEGIDA</text>
  <line x1="2.0" y1="29.5" x2="134.38" y2="29.5" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="31.0" width="132.38" height="5.0" fill="#333333" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">ESPÉCIE / NOME CIENTÍFICO</text>
  <text x="56.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">HÁBITAT DE REPRODUÇÃO</text>
  <text x="96.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">STATUS DE CONSERVAÇÃO</text>
  <text x="132.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff" text-anchor="end">REGISTROS</text>
''')
    species_rows = [
        ("Tartaruga-da-amazônia (P. expansa)", "Altos de praias arenosas e tabuleiros", "Sítio reprodutivo crítico / Ameaçada", "Principal", "#ffffff"),
        ("Tracajá (Podocnemis unifilis)", "Bancos de areia e margens de igarapé", "Vulnerável / Intensa postura local", "Abundante", "#f8f9fa"),
        ("Pitiú / Iaçá (P. sextuberculata)", "Bancos arenosos baixos e saibro fino", "Espécie protegida de menor porte", "Frequente", "#ffffff"),
        ("Curimatá (Prochilodus nigricans)", "Furos e canais de ligação de várzea", "Ictiofauna reofílica / Desova mapeada", "04 Pontos", "#f8f9fa"),
        ("Peixe-boi da Amazônia (T. inunguis)", "Igarapé Japopaca e Lago Pitoa", "Mamífero aquático / Área de refúgio", "Refúgio", "#ffffff")
    ]
    cur_y = 36.0
    for name, hab, stat, reg, bg in species_rows:
        svg.append(f'''  <rect x="2.0" y="{cur_y:.2f}" width="132.38" height="5.5" fill="{bg}" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="{cur_y + 3.8:.2f}" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">{name}</text>
  <text x="56.0" y="{cur_y + 3.8:.2f}" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">{hab}</text>
  <text x="96.0" y="{cur_y + 3.8:.2f}" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">{stat}</text>
  <text x="132.0" y="{cur_y + 3.8:.2f}" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">{reg}</text>''')
        cur_y += 5.5

    # 3. CRONOGRAMA FENOLÓGICO
    svg.append(f'''
  <!-- 3. CALENDÁRIO REPRODUTIVO -->
  <text x="2.0" y="66.5" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">CALENDÁRIO REPRODUTIVO DOS QUELÔNIOS E REGIME DO RIO XINGU</text>
  <line x1="2.0" y1="68.0" x2="134.38" y2="68.0" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="69.5" width="132.38" height="42.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />

  <!-- Bloco 1 -->
  <rect x="4.0" y="71.5" width="40.0" height="38.0" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <rect x="4.0" y="71.5" width="40.0" height="2.0" fill="#d48b00" stroke="none" rx="0" ry="0" />
  <text x="6.5" y="76.5" font-family="{FONT}" font-size="2.1" font-weight="600" fill="#d48b00">1. VAZANTE / POSTURA</text>
  <text x="6.5" y="80.5" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#212529">Período: Agosto a Outubro</text>
  <text x="6.5" y="84.5" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Queda da lâmina do Rio Xingu;</text>
  <text x="6.5" y="88.0" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Emersão dos bancos arenosos;</text>
  <text x="6.5" y="91.5" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Subida noturna das fêmeas;</text>
  <text x="6.5" y="95.0" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Escavação de covas e postura;</text>
  <text x="6.5" y="98.5" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Máxima vigilância do IDEFLOR;</text>
  <text x="6.5" y="102.0" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Combate à coleta predatória.</text>

  <!-- Bloco 2 -->
  <rect x="48.0" y="71.5" width="40.0" height="38.0" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <rect x="48.0" y="71.5" width="40.0" height="2.0" fill="#007f5f" stroke="none" rx="0" ry="0" />
  <text x="50.5" y="76.5" font-family="{FONT}" font-size="2.1" font-weight="600" fill="#007f5f">2. ECLOSÃO / RECRUTAMENTO</text>
  <text x="50.5" y="80.5" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#212529">Período: Novembro a Janeiro</text>
  <text x="50.5" y="84.5" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Incubação térmica de ~60 dias;</text>
  <text x="50.5" y="88.0" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Nascimento massivo dos filhotes;</text>
  <text x="50.5" y="91.5" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Corrida sincronizada para a água;</text>
  <text x="50.5" y="95.0" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Manejo de soltura e biometria;</text>
  <text x="50.5" y="98.5" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Monitoramento de predadores;</text>
  <text x="50.5" y="102.0" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Integração com voluntários locais.</text>

  <!-- Bloco 3 -->
  <rect x="92.0" y="71.5" width="40.0" height="38.0" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <rect x="92.0" y="71.5" width="40.0" height="2.0" fill="#1864ab" stroke="none" rx="0" ry="0" />
  <text x="94.5" y="76.5" font-family="{FONT}" font-size="2.1" font-weight="600" fill="#1864ab">3. CHEIA / ALIMENTAÇÃO</text>
  <text x="94.5" y="80.5" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#212529">Período: Fevereiro a Julho</text>
  <text x="94.5" y="84.5" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Subida das águas e inundação;</text>
  <text x="94.5" y="88.0" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Desaparecimento dos tabuleiros;</text>
  <text x="94.5" y="91.5" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Dispersão para furos e igapós;</text>
  <text x="94.5" y="95.0" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Alimentação em matas de várzea;</text>
  <text x="94.5" y="98.5" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Consumo de frutos florestais;</text>
  <text x="94.5" y="102.0" font-family="{FONT}" font-size="1.85" font-weight="600" fill="#495057">• Fase de crescimento e engorda.</text>

  <!-- 4. PATRIMÔNIO FLORÍSTICO -->
  <text x="2.0" y="115.5" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">PATRIMÔNIO FLORÍSTICO E ÁRVORES MATRIZES (50 REGISTROS)</text>
  <line x1="2.0" y1="117.0" x2="134.38" y2="117.0" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="118.5" width="132.38" height="5.0" fill="#495057" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="122.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">ESPÉCIE BOTÂNICA</text>
  <text x="56.0" y="122.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">NOME CIENTÍFICO</text>
  <text x="96.0" y="122.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">TIPOLOGIA FLORESTAL</text>
  <text x="132.0" y="122.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff" text-anchor="end">IMPORTÂNCIA</text>

  <rect x="2.0" y="123.5" width="132.38" height="5.5" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="127.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Seringueira com Lanho</text>
  <text x="56.0" y="127.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Hevea brasiliensis</text>
  <text x="96.0" y="127.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Floresta Aluvial de Várzea</text>
  <text x="132.0" y="127.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">Extrativismo / Histórico</text>

  <rect x="2.0" y="129.0" width="132.38" height="5.5" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="132.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Jatobá</text>
  <text x="56.0" y="132.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Hymenaea courbaril</text>
  <text x="96.0" y="132.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Mata de Terra Firme / Transição</text>
  <text x="132.0" y="132.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">Matriz / Alimento Fauna</text>

  <rect x="2.0" y="134.5" width="132.38" height="5.5" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="138.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Castanheira-do-Pará</text>
  <text x="56.0" y="138.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Bertholletia excelsa</text>
  <text x="96.0" y="138.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Terra Firme Adjacente</text>
  <text x="132.0" y="138.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">Espécie Imune de Corte</text>

  <rect x="2.0" y="142.0" width="132.38" height="32.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <text x="4.0" y="146.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40"><b>Relação Ecológica entre a Floresta e os Quelônios:</b> As florestas ripárias e matas de várzea do mosaico de UCs</text>
  <text x="4.0" y="150.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">são componentes fundamentais do ciclo de vida das espécies aquáticas. Durante o período de cheia, os quelônios</text>
  <text x="4.0" y="154.1" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">adentram a floresta alagada para consumir frutos caídos, sementes e brotos, estocando energia para a postura.</text>
  <text x="4.0" y="157.9" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">A conservação da vegetação arbórea nas margens das ilhas (como Goiabal e Mungubal) assegura a estabilidade térmica,</text>
  <text x="4.0" y="161.7" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">evita a erosão eólica das dunas e retém sedimentos que formam as praias reprodutivas do Tabuleiro do Embaubal.</text>
  <text x="4.0" y="165.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">O georreferenciamento de matrizes permite monitorar a integridade florística e combater a extração seletiva ilegal.</text>

  <!-- RODAPÉ TÉCNICO -->
  <line x1="2.0" y1="176.0" x2="134.38" y2="176.0" stroke="#ced4da" stroke-width="0.3" />
  <text x="2.0" y="180.0" font-family="{FONT}" font-size="1.75" font-weight="600" fill="#6c757d">Fonte: Monitoramento de Quelônios e Botânica IDEFLOR-Bio (2025-2026). Sistema Geodésico: SIRGAS 2000 UTM 22S.</text>
  <text x="2.0" y="183.2" font-family="{FONT}" font-size="1.75" font-weight="600" fill="#6c757d">Refúgio de Vida Silvestre Tabuleiro do Embaubal. Diretoria de Gestão da Biodiversidade (DGBIO). Cartografia A1.</text>''')
    svg.append(get_footer())
    return "\n".join(svg)


# ==============================================================================
# PAINEL 04: COMUNIDADES E USO TRADICIONAL
# ==============================================================================
def gen_panel_04():
    w, h = 136.382, 186.572
    svg = [get_header(w, h)]
    
    # 1. INDICADORES
    svg.append(f'''  <!-- 1. INDICADORES SOCIOESPACIAIS -->
  <rect x="2.0" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="2.0" width="42.79" height="1.8" fill="#e65100" stroke="none" rx="0" ry="0" />
  <text x="23.4" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#e65100" text-anchor="middle">282</text>
  <text x="23.4" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">MORADIAS RIBEIRINHAS</text>
  <text x="23.4" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">Famílias Cadastradas</text>

  <rect x="46.79" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="46.79" y="2.0" width="42.79" height="1.8" fill="#00838f" stroke="none" rx="0" ry="0" />
  <text x="68.19" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#00838f" text-anchor="middle">89</text>
  <text x="68.19" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">APOIOS DE PESCA</text>
  <text x="68.19" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">Ranchos Mapeados</text>

  <rect x="91.58" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="91.58" y="2.0" width="42.79" height="1.8" fill="#2e7d32" stroke="none" rx="0" ry="0" />
  <text x="112.98" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#2e7d32" text-anchor="middle">100%</text>
  <text x="112.98" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">USO SUSTENTÁVEL</text>
  <text x="112.98" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">RDS Vitória de Souzel</text>

  <!-- 2. CENSO E TIPOLOGIA -->
  <text x="2.0" y="28.0" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">CENSO SOCIOESPACIAL E ESTRUTURAS ANTRÓPICAS</text>
  <line x1="2.0" y1="29.5" x2="134.38" y2="29.5" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="31.0" width="132.38" height="5.0" fill="#333333" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">CATEGORIA DE ESTRUTURA</text>
  <text x="56.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">REGIME DE OCUPAÇÃO</text>
  <text x="96.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">DISTRIBUIÇÃO ESPACIAL</text>
  <text x="132.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff" text-anchor="end">TOTAL</text>
''')
    socio_rows = [
        ("Residências Ribeirinhas Permanentes", "Permanente / Familiar", "Margens de rios, furos e restingas insulares", "282", "#ffffff"),
        ("Ranchos de Apoio de Pesca Ativos", "Sazonal / Período de Safra", "Próximo a pesqueiros, saídas de furos e canais", "89", "#f8f9fa"),
        ("Escolas Rurais Comunitárias", "Ano Letivo / Comunitário", "Polos concentradores (ex: Sol Elarrant Canto)", "Cadastradas", "#ffffff"),
        ("Igrejas e Centros Comunitários", "Eventos / Festividades", "Comunidade São Marcos, Carmelita e vilarejos", "Cadastradas", "#f8f9fa"),
        ("Total de Pontos de Uso Comunitário", "Socioeconomia Tradicional", "Território integral da RDS Vitória de Souzel", "371", "#e9ecef")
    ]
    cur_y = 36.0
    for cat, reg, dist, total, bg in socio_rows:
        svg.append(f'''  <rect x="2.0" y="{cur_y:.2f}" width="132.38" height="5.5" fill="{bg}" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="{cur_y + 3.8:.2f}" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">{cat}</text>
  <text x="56.0" y="{cur_y + 3.8:.2f}" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">{reg}</text>
  <text x="96.0" y="{cur_y + 3.8:.2f}" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">{dist}</text>
  <text x="132.0" y="{cur_y + 3.8:.2f}" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">{total}</text>''')
        cur_y += 5.5

    # 3. PROPORÇÃO DE USO
    svg.append(f'''
  <!-- 3. PROPORÇÃO DE USO -->
  <text x="2.0" y="66.5" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">ESTRUTURA DA OCUPAÇÃO RURAL E PESQUEIRA</text>
  <line x1="2.0" y1="68.0" x2="134.38" y2="68.0" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="69.5" width="132.38" height="21.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <text x="5.0" y="73.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Residências Ribeirinhas (Habitação Permanente): 76,01% (282 pontos)</text>
  <rect x="5.0" y="75.0" width="100.6" height="4.0" fill="#e65100" stroke="#333333" stroke-width="0.2" rx="0" ry="0" />
  <rect x="105.6" y="75.0" width="23.78" height="4.0" fill="#e9ecef" stroke="#ced4da" stroke-width="0.2" rx="0" ry="0" />

  <text x="5.0" y="83.2" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Ranchos de Pesca (Estruturas Sazonais de Apoio): 23,99% (89 pontos)</text>
  <rect x="5.0" y="84.5" width="31.75" height="4.0" fill="#00838f" stroke="#333333" stroke-width="0.2" rx="0" ry="0" />
  <rect x="36.75" y="84.5" width="92.63" height="4.0" fill="#e9ecef" stroke="#ced4da" stroke-width="0.2" rx="0" ry="0" />

  <!-- 4. DIRETRIZES DE MANEJO E PESCA -->
  <text x="2.0" y="94.5" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">DINÂMICA DA PESCA ARTESANAL E MANEJO PARTICIPATIVO</text>
  <line x1="2.0" y1="96.0" x2="134.38" y2="96.0" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="97.5" width="132.38" height="35.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="97.5" width="2.5" height="35.0" fill="#00838f" stroke="none" rx="0" ry="0" />
  <text x="6.5" y="102.0" font-family="{FONT}" font-size="2.2" font-weight="600" fill="#00838f">PRÁTICAS DE PESCA TRADICIONAL NA RDS VITÓRIA DE SOUZEL</text>
  <text x="6.5" y="106.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Equipamentos Empregados:</b> Malhadeiras com malhagem regulamentada, espinhéis, linhas de mão e tarrafas.</text>
  <text x="6.5" y="110.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Ictiofauna Alvo de Manejo:</b> Curimatá, pacu, tucunaré, filhote/piraíba, pirarucu, aracu e surubim.</text>
  <text x="6.5" y="114.1" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Função dos Ranchos Pesqueiros:</b> Pouso de vigília, estaleiro para secagem de malhadeiras e salga do peixe.</text>
  <text x="6.5" y="117.9" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Proteção aos Quelônios:</b> O consumo de carne ou ovos de tartaruga é proibido pelas normas da unidade.</text>
  <text x="6.5" y="121.7" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Segurança Territorial:</b> A delimitação da RDS consolidou a garantia dos territórios das famílias tradicionais.</text>
  <text x="6.5" y="125.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Comercialização:</b> O excedente da pesca abastece feiras em Senador José Porfírio, Porto de Moz e Vitória do Xingu.</text>

  <!-- 5. GESTÃO PARTICIPATIVA E CONSELHO -->
  <rect x="2.0" y="136.0" width="132.38" height="38.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="136.0" width="2.5" height="38.0" fill="#e65100" stroke="none" rx="0" ry="0" />
  <text x="6.5" y="140.5" font-family="{FONT}" font-size="2.2" font-weight="600" fill="#e65100">CONSELHO GESTOR E ALIANÇA CONSERVACIONISTA</text>
  <text x="6.5" y="145.0" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">A governança da RDS Vitória de Souzel assenta-se na participação democrática das comunidades locais.</text>
  <text x="6.5" y="148.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">O Conselho Gestor paritário delibera sobre acordos de pesca, zoneamento de furos e épocas de defeso.</text>
  <text x="6.5" y="152.6" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">Existe uma sinergia direta e indissociável entre a RDS e o REVIS Tabuleiro do Embaubal: os moradores das</text>
  <text x="6.5" y="156.4" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">ilhas atuam ativamente como voluntários no monitoramento dos tabuleiros de desova, auxiliando os fiscais.</text>
  <text x="6.5" y="160.2" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">A permanência digna das populações tradicionais com acesso a escolas e saúde constitui a principal barreira</text>
  <text x="6.5" y="164.0" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">contra o avanço do desmatamento ilegal, invasões fundiárias e garimpos clandestinos no Baixo Xingu.</text>
  <text x="6.5" y="167.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">O cadastramento georreferenciado permite ao Estado planejar políticas públicas direcionadas e inclusivas.</text>

  <!-- RODAPÉ TÉCNICO -->
  <line x1="2.0" y1="176.0" x2="134.38" y2="176.0" stroke="#ced4da" stroke-width="0.3" />
  <text x="2.0" y="180.0" font-family="{FONT}" font-size="1.75" font-weight="600" fill="#6c757d">Fonte: Cadastro Socioambiental e de Moradores IDEFLOR-Bio (2025-2026). Sistema Geodésico: SIRGAS 2000 UTM 22S.</text>
  <text x="2.0" y="183.2" font-family="{FONT}" font-size="1.75" font-weight="600" fill="#6c757d">Reserva de Desenvolvimento Sustentável Vitória de Souzel. Diretoria de Gestão e Monitoramento de UCs (DGBIO/GRB).</text>''')
    svg.append(get_footer())
    return "\n".join(svg)


# ==============================================================================
# PAINEL 05: GEOGRAFIA E HIDROGRAFIA
# ==============================================================================
def gen_panel_05():
    w, h = 136.382, 186.572
    svg = [get_header(w, h)]
    
    # 1. INDICADORES
    svg.append(f'''  <!-- 1. INDICADORES HIDROMORFOLÓGICOS -->
  <rect x="2.0" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="2.0" width="42.79" height="1.8" fill="#0077b6" stroke="none" rx="0" ry="0" />
  <text x="23.4" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#0077b6" text-anchor="middle">134</text>
  <text x="23.4" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">CORPOS HÍDRICOS</text>
  <text x="23.4" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">Rios, Furos e Igarapés</text>

  <rect x="46.79" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="46.79" y="2.0" width="42.79" height="1.8" fill="#b07d4b" stroke="none" rx="0" ry="0" />
  <text x="68.19" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#b07d4b" text-anchor="middle">78</text>
  <text x="68.19" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">ILHAS E PRAIAS</text>
  <text x="68.19" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">Mosaico de Areia e Várzea</text>

  <rect x="91.58" y="2.0" width="42.79" height="20.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="91.58" y="2.0" width="42.79" height="1.8" fill="#495057" stroke="none" rx="0" ry="0" />
  <text x="112.98" y="10.5" font-family="{FONT}" font-size="4.6" font-weight="600" fill="#495057" text-anchor="middle">16</text>
  <text x="112.98" y="15.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#495057" text-anchor="middle">MARCOS NÁUTICOS</text>
  <text x="112.98" y="18.5" font-family="{FONT}" font-size="1.8" font-weight="600" fill="#868e96" text-anchor="middle">Canais e Referências</text>

  <!-- 2. HIERARQUIA HÍDRICA -->
  <text x="2.0" y="28.0" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">HIERARQUIA E CLASSIFICAÇÃO DA REDE HIDROGRÁFICA</text>
  <line x1="2.0" y1="29.5" x2="134.38" y2="29.5" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="31.0" width="132.38" height="5.0" fill="#333333" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">TIPOLOGIA HÍDRICA</text>
  <text x="46.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">CARACTERÍSTICA DINÂMICA</text>
  <text x="96.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">EXEMPLOS PRINCIPAIS</text>
  <text x="132.0" y="34.5" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff" text-anchor="end">PONTOS</text>
''')
    hydro_rows = [
        ("Rios Principais / Calha", "Vias navegáveis estruturantes perenes", "Rio Xingu, Rio Cacau, Rio Arapari, Rio Tamanduá", "27", "#ffffff"),
        ("Furos Fluviais (Atalhos)", "Canais que cortam ilhas e conectam braços", "Furo Bom Jardim, Camaleoa, Tapecurá, Goiabal", "33", "#f8f9fa"),
        ("Igarapés de Várzea e Igapó", "Drenagem interna e florestal de médio porte", "Igarapé Atuca, Japopaca, Pitoa, Santa Tereza", "28", "#ffffff"),
        ("Lagos e Ressacos de Várzea", "Corpos lentos de alimentação e refúgio", "Lago Aramamba, Lago Pitoa, Lago do Palhau", "07", "#f8f9fa"),
        ("Poços Artesianos e Cacimbas", "Captação de água doce subterrânea", "Poço da Lama, Poço dos Porunas", "03", "#ffffff")
    ]
    cur_y = 36.0
    for cat, dyn, ex, count, bg in hydro_rows:
        svg.append(f'''  <rect x="2.0" y="{cur_y:.2f}" width="132.38" height="5.5" fill="{bg}" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="{cur_y + 3.8:.2f}" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">{cat}</text>
  <text x="46.0" y="{cur_y + 3.8:.2f}" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">{dyn}</text>
  <text x="96.0" y="{cur_y + 3.8:.2f}" font-family="{FONT}" font-size="1.9" font-weight="600" fill="#495057">{ex}</text>
  <text x="132.0" y="{cur_y + 3.8:.2f}" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">{count}</text>''')
        cur_y += 5.5

    # 3. MORFOLOGIA INSULAR
    svg.append(f'''
  <!-- 3. MORFOLOGIA INSULAR -->
  <text x="2.0" y="66.5" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">MORFOLOGIA INSULAR E PRAIAS FLUVIAIS (78 PONTOS)</text>
  <line x1="2.0" y1="68.0" x2="134.38" y2="68.0" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="69.5" width="132.38" height="5.0" fill="#495057" stroke="none" rx="0" ry="0" />
  <text x="4.0" y="73.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">FEIÇÃO MORFOLÓGICA</text>
  <text x="50.0" y="73.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">PAPEL ECOLÓGICO E NAVEGAÇÃO</text>
  <text x="96.0" y="73.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff">PRINCIPAIS REGISTROS</text>
  <text x="132.0" y="73.0" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#ffffff" text-anchor="end">STATUS</text>

  <rect x="2.0" y="74.5" width="132.38" height="5.5" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="78.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Grandes Ilhas Aluviais</text>
  <text x="50.0" y="78.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Ilhas estáveis com matas densas de várzea</text>
  <text x="96.0" y="78.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Ilha Embaubal, Abaeté, Cipó Pitanga</text>
  <text x="132.0" y="78.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">Perene</text>

  <rect x="2.0" y="80.0" width="132.38" height="5.5" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="83.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Ilhas Menores e Ilhotas</text>
  <text x="50.0" y="83.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Refúgio de fauna e divisórias de canais</text>
  <text x="96.0" y="83.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Ilha da Preguiça, Goiabal, Mungubal</text>
  <text x="132.0" y="83.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">Perene</text>

  <rect x="2.0" y="85.5" width="132.38" height="5.5" fill="#ffffff" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="89.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Praias Fluviais e Pontas</text>
  <text x="50.0" y="89.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Sedimentação de areia grossa e média</text>
  <text x="96.0" y="89.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Praia do Gigi, Ponta do Navio, Paneminha</text>
  <text x="132.0" y="89.3" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">Sazonal</text>

  <rect x="2.0" y="91.0" width="132.38" height="5.5" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.25" rx="0" ry="0" />
  <text x="4.0" y="94.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529">Bancos de Areia Emersos</text>
  <text x="50.0" y="94.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Áreas de nidificação de quelônios e aves</text>
  <text x="96.0" y="94.8" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#495057">Bancos da Boca das Ilhas e Meio do Rio</text>
  <text x="132.0" y="94.8" font-family="{FONT}" font-size="2.0" font-weight="600" fill="#212529" text-anchor="end">Sazonal</text>

  <!-- 4. PULSO DE INUNDAÇÃO -->
  <text x="2.0" y="100.5" font-family="{FONT}" font-size="2.8" font-weight="600" fill="#212529">PULSO DE INUNDAÇÃO DO BAIXO XINGU E DINÂMICA SEDIMENTAR</text>
  <line x1="2.0" y1="102.0" x2="134.38" y2="102.0" stroke="#333333" stroke-width="0.5" />

  <rect x="2.0" y="103.5" width="132.38" height="32.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="103.5" width="2.5" height="32.0" fill="#0077b6" stroke="none" rx="0" ry="0" />
  <text x="6.5" y="108.0" font-family="{FONT}" font-size="2.2" font-weight="600" fill="#0077b6">VARIAÇÃO HIDROMÉTRICA SAZONAL (4 A 6 METROS DE AMPLITUDE)</text>
  <text x="6.5" y="112.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Estiagem (Agosto - Novembro):</b> Queda acentuada da lâmina d'água; formação dos extensos tabuleiros de areia</text>
  <text x="6.5" y="116.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">  e fechamento de furos rasos, concentrando a navegação nos canais de maior profundidade balizados por faróis.</text>
  <text x="6.5" y="120.1" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Cheia (Fevereiro - Junho):</b> Elevação do nível das águas, afogamento completo dos bancos arenosos e abertura de</text>
  <text x="6.5" y="123.9" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">  todos os furos navegáveis, conectando o rio principal aos lagos de várzea internos e florestas de igapó.</text>
  <text x="6.5" y="127.7" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Morfodinâmica dos Sedimentos:</b> O transporte de sedimentos de fundo do Xingu reconstitui as praias anualmente.</text>
  <text x="6.5" y="131.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">• <b>Conectividade de Habitats:</b> A pulsação hídrica oxigena os lagos e promove a troca de nutrientes da biomassa.</text>

  <!-- 5. NAVEGABILIDADE E MARCOS -->
  <rect x="2.0" y="138.5" width="132.38" height="35.0" fill="#f8f9fa" stroke="#ced4da" stroke-width="0.3" rx="0" ry="0" />
  <rect x="2.0" y="138.5" width="2.5" height="35.0" fill="#b07d4b" stroke="none" rx="0" ry="0" />
  <text x="6.5" y="143.0" font-family="{FONT}" font-size="2.2" font-weight="600" fill="#b07d4b">NAVEGABILIDADE E MARCOS NÁUTICOS DE REFERÊNCIA (16 PONTOS)</text>
  <text x="6.5" y="147.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">O complexo arquipélago fluvial e os extensos bancos de areia móveis tornam a navegação no Baixo Xingu</text>
  <text x="6.5" y="151.3" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">dependente de marcos de referência bem estabelecidos: as bocas de furos (como a Boca do Juncal, Furo da Camaleoa,</text>
  <text x="6.5" y="155.1" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">Furo Bom Jardim), as passagens estreitas de canal (Canal do Sacrifício) e o Farol de Canal são referências</text>
  <text x="6.5" y="158.9" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">indispensáveis para evitar encalhes de embarcações maiores da fiscalização ambiental e de transporte regional.</text>
  <text x="6.5" y="162.7" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">A dinâmica dos canais é monitorada para orientar os pilotos de lanchas durante operações noturnas na desova.</text>
  <text x="6.5" y="166.5" font-family="{FONT}" font-size="1.95" font-weight="600" fill="#343a40">Os registros constituem patrimônio toponímico hidrográfico oficial registrado pelo IDEFLOR-Bio.</text>

  <!-- RODAPÉ TÉCNICO -->
  <line x1="2.0" y1="176.0" x2="134.38" y2="176.0" stroke="#ced4da" stroke-width="0.3" />
  <text x="2.0" y="180.0" font-family="{FONT}" font-size="1.75" font-weight="600" fill="#6c757d">Fonte: Cartografia Hidrográfica e Morfológica IDEFLOR-Bio (2025-2026). Sistema Geodésico: SIRGAS 2000 UTM 22S.</text>
  <text x="2.0" y="183.2" font-family="{FONT}" font-size="1.75" font-weight="600" fill="#6c757d">Mosaico REVIS Tabuleiro do Embaubal e RDS Vitória de Souzel. Bacia do Rio Xingu, Pará. Cartografia A1.</text>''')
    svg.append(get_footer())
    return "\n".join(svg)


# Build and save all 5 files
panels = [
    ("01_limites_e_unidades_conservacao.svg", gen_panel_01()),
    ("02_gestao_e_infraestrutura.svg", gen_panel_02()),
    ("03_biodiversidade_e_protecao_ambiental.svg", gen_panel_03()),
    ("04_comunidades_e_uso_tradicional.svg", gen_panel_04()),
    ("05_geografia_e_hidrografia.svg", gen_panel_05())
]

for fname, content in panels:
    path = os.path.join(output_dir, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated: {path} ({len(content)} bytes)")

print("\nAll 5 SVGs written. Testing rendering with Qt QSvgRenderer...")
