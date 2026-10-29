# -*- coding: utf-8 -*-
"""
Geração do Relatório Técnico Oficial em formato DOCX (.docx)
Tema: Tratamento Cartográfico, Deduplicação Espacial e Depuração de Dados de Campo
Unidades: REVIS Tabuleiro do Embaubal e RDS Vitória de Souzel
Padrão Institucional: NGEO / IDEFLOR-Bio (Arial 12, Justificado, 1.5 entrelinhas, cabeçalho oficial)
"""

import os
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

TEMPLATE_PATH = "H:/Meu Drive/DEV/qgis-layout-engine/relatorios/relatorio.docx"
DIR_RELATORIOS = "relatorios"
OUTPUT_PATH = "relatorios/Relatorio_Tecnico_Limpeza_e_Deduplicacao_Pontos_NGEO.docx"
OUTPUT_ROOT = "Relatorio_Tecnico_Limpeza_e_Deduplicacao_Pontos_NGEO.docx"

os.makedirs(DIR_RELATORIOS, exist_ok=True)

# 1. Carrega o documento matriz
doc = docx.Document(TEMPLATE_PATH)

# Remove conteúdo anterior do corpo (preservando cabeçalho oficial header1.xml)
for p in list(doc.paragraphs):
    p._element.getparent().remove(p._element)

for t in list(doc.tables):
    t._element.getparent().remove(t._element)

# Funções auxiliares de formatação ABNT / NGEO
def add_titulo(texto):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(texto)
    run.font.name = "Arial"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(27, 54, 38) # Verde Floresta Escuro
    return p

def add_subtitulo(texto):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(16)
    run = p.add_run(texto)
    run.font.name = "Arial"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(80, 80, 80)
    return p

def add_secao(numero_e_titulo):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(numero_e_titulo)
    run.font.name = "Arial"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(27, 54, 38)
    return p

def add_subsecao(texto):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(texto)
    run.font.name = "Arial"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(40, 40, 40)
    return p

def add_paragrafo(texto):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(texto)
    run.font.name = "Arial"
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(30, 30, 30)
    return p

def add_item_lista(titulo_item, texto_item):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.first_line_indent = Inches(-0.2)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.3
    r_bullet = p.add_run("• ")
    r_bullet.font.name = "Arial"
    r_bullet.font.size = Pt(11.5)
    r_bullet.font.bold = True
    r_bullet.font.color.rgb = RGBColor(27, 54, 38)
    r1 = p.add_run(titulo_item + ": ")
    r1.font.name = "Arial"
    r1.font.size = Pt(11.5)
    r1.font.bold = True
    r2 = p.add_run(texto_item)
    r2.font.name = "Arial"
    r2.font.size = Pt(11.5)
    return p

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

# -------------------------------------------------------------------------
# CORPO DO RELATÓRIO TÉCNICO
# -------------------------------------------------------------------------

# Título Principal
add_titulo("RELATÓRIO TÉCNICO")
add_subtitulo("TRATAMENTO CARTOGRÁFICO, DEDUPLICAÇÃO ESPACIAL E DEPURAÇÃO DE DADOS VETORIAIS DE CAMPO\nREVIS TABULEIRO DO EMBAUBAL E RDS VITÓRIA DE SOUZEL")

# 1. Identificação
add_secao("1. Identificação do Documento")
add_item_lista("Processo Administrativo", "Processo de Elaboração do Plano de Gestão Territorial nº 2026/3605158")
add_item_lista("Unidades Objeto", "Refúgio de Vida Silvestre (REVIS) Tabuleiro do Embaubal e Reserva de Desenvolvimento Sustentável (RDS) Vitória de Souzel")
add_item_lista("Órgão Gestor / Demandante", "Diretoria de Gestão e Monitoramento de Unidades de Conservação – DGMUC / IDEFLOR-Bio")
add_item_lista("Setor Executor", "Núcleo de Geotecnologias – NGEO / IDEFLOR-Bio")
add_item_lista("Responsável Técnico", "Samuel da Costa dos Santos – Coordenador do Núcleo de Geotecnologias")
add_item_lista("Sistema de Referência Geodésica", "SIRGAS 2000 / Projeção Universal Transversa de Mercator (UTM), Zona 22 Sul (EPSG: 31982)")
add_item_lista("Data de Elaboração", "Outubro de 2026")

# 2. Objetivos
add_secao("2. Objetivos")
add_paragrafo(
    "O presente Relatório Técnico tem por objetivo documentar e homologar os procedimentos metodológicos "
    "de depuração, controle de qualidade topológica, deduplicação espacial de passadas múltiplas e "
    "padronização toponímica aplicados ao acervo de dados geoespaciais vetoriais de campo. O estudo "
    "abrange o território consolidado do Refúgio de Vida Silvestre (REVIS) Tabuleiro do Embaubal (4.035,71 ha) "
    "e da Reserva de Desenvolvimento Sustentável (RDS) Vitória de Souzel (22.987,41 ha), localizados na calha "
    "do Baixo Rio Xingu, no Estado do Pará, fornecendo subsídios auditados para a série cartográfica oficial "
    "e para o respectivo Plano de Gestão Territorial."
)

# 3. Contextualização
add_secao("3. Contextualização")
add_paragrafo(
    "Durante as expedições de levantamento de campo coordenadas pelas equipes técnicas do IDEFLOR-Bio "
    "(equipes de coleta de dados de campo das técnicas Lorena e Kelly), foram registrados pontos de interesse "
    "geográfico distribuídos em diversas categorias temáticas: moradores e comunidades ribeirinhas, apoios de pesca "
    "e ranchos sazonais, praias e áreas de desova de quelônios, acidentes hidrográficos (furos e igarapés), "
    "infraestruturas comunitárias e marcos referenciais de navegação."
)
add_paragrafo(
    "Em razão da complexidade da malha hídrica do Baixo Xingu e da realização de levantamentos contínuos por "
    "diferentes equipes ao longo das calhas dos rios e furos em trajetos de ida e volta, verificou-se a "
    "existência de feições redundantes registradas em duplicidade métrica (mesmo local físico cadastrado com "
    "ligeiras variações toponímicas ou duplicado com poucos metros de afastamento). Adicionalmente, identificou-se "
    "a incorporação indevida de waypoints automáticos de deslocamento gerados por aparelhos receptores GPS "
    "e aplicativos de monitoramento de percurso (rotulados automaticamente como registros de atividades, "
    "dias da semana e paradas de rotina), os quais não constituem infraestrutura de acesso ou pontos de uso "
    "territorial legítimos."
)
add_paragrafo(
    "Diante disso, fez-se mandatória a aplicação de rotina computacional automatizada no Núcleo de Geotecnologias "
    "para assegurar a higienização integral da base vetorial, eliminando ruídos estatísticos e prevenindo "
    "a sobreposição de marcadores na composição das pranchas cartográficas institucionais padronizadas."
)

# 4. Procedimentos Realizados
add_secao("4. Procedimentos Realizados")
add_paragrafo(
    "As etapas de auditoria, limpeza e enriquecimento cartográfico foram estruturadas em ambiente computacional "
    "SIG (Python 3.12, GeoPandas, Shapely e SciPy Spatial) integrado ao Sistema de Informação Geográfica QGIS 3.34 LTR / 4.x, "
    "obedecendo ao seguinte encadeamento técnico:"
)

add_item_lista(
    "a) Salvaguarda Integral da Base Bruta",
    "Previamente a qualquer manipulação de dados, todas as camadas vetoriais de entrada foram arquivadas em diretório "
    "de contingência e auditoria ('camadas/backup_pre_limpeza/'), assegurando rastreabilidade irrestrita de todas "
    "as coordenadas originais coletadas em campo."
)

add_item_lista(
    "b) Filtragem de Paradas Espúrias e Padronização da Camada de Acessos",
    "A camada temática de acessos ('10_trajetos_e_acessos.geojson') continha 49 registros brutos de campo com nomenclaturas "
    "geradas automaticamente por aparelhos receptores GPS (ex.: 'quarta-feira Afternoon Activity', 'quinta-feira Morning Pesca'). "
    "Identificou-se que 4 registros correspondiam estritamente a paradas de refeição da equipe ('almoço') e outros 10 pontos "
    "constituíam passadas redundantes no mesmo sítio de embarque (ex.: 5 passadas sobrepostas na Base Fluvial). "
    "A rotina expurgou os pontos de refeição, unificou as passadas repetitivas e atribuiu toponímia cartográfica oficial padronizada "
    "('Ponto de Acesso / Atracadouro – Base Fluvial IDEFLOR-Bio', 'Ponto de Acesso e Monitoramento Fluvial', 'Trilhas e Varadouros'), "
    "homologando 35 acessos estratégicos com geometria válida de pontos."
)

add_item_lista(
    "c) Deduplicação Espacial Baseada em Proximidade Euclidiana (cKDTree)",
    "Para cada uma das camadas temáticas pontuais, realizou-se a projeção para o sistema métrico SIRGAS 2000 / UTM 22S (EPSG: 31982) "
    "e a indexação espacial das coordenadas por meio de árvores multidimensionais de busca ('cKDTree'). Estabeleceu-se o raio de "
    "tolerância euclidiana máxima de 25 metros para a detecção de passadas redundantes no mesmo sítio geográfico."
)

add_item_lista(
    "d) Critério Toponímico de Seleção da Feição Válida",
    "Identificados pares de pontos sobrepostos ou vizinhos em distância inferior a 25 metros, o algoritmo avaliou o grau de "
    "completude toponímica de cada feição. Estabeleceu-se como diretriz mandatória a preservação do registro com maior riqueza "
    "descritiva e denominação formal de moradores/famílias, eliminando-se a feição simplificada ou rotulada com termos genéricos "
    "(exemplo: preservado 'Joelma do Socorro Firmino da Rocha' e descartado 'Joelma do Socorro'; preservado 'Bito - Benedito Ferreira de Souza' "
    "e descartado 'Bito'; preservado 'Rancho do Josiel Duarte da Rocha (Jojoca)' e descartado 'Josiel Duarte da Rocha')."
)

add_item_lista(
    "e) Refinamento da Simbologia de Quelônios na Prancha Cartográfica",
    "Atendendo à necessidade de destaque das praias de desova de quelônios (Tartaruga-da-Amazônia e Tracajá) — vocação primária "
    "do REVIS Tabuleiro do Embaubal —, procedeu-se ao redimensionamento do símbolo composto na camada 'Áreas de Desova (Quelônios e Peixes)': "
    "o marcador de fundo ('SimpleMarker') foi ampliado de 6,7 mm para 10,5 mm (com borda de 1,0 mm), e o ícone vetorial da tartaruga "
    "('SvgMarker') foi expandido de 5,5 mm para 8,8 mm, garantindo excelente visibilidade e hierarquia visual na prancha impressa."
)

add_item_lista(
    "f) Instituição de Marcador Nobre para a Base Operacional do IDEFLOR-Bio",
    "Substituiu-se o marcador circular genérico anterior (3,2 mm) da camada 'BASE DO IDEFLOR-BIO' por um elemento cartográfico "
    "emblema de três níveis: círculo de fundo verde floresta institucional (#0E4D2A) com 11,5 mm de diâmetro e moldura dourada (#F1C40F) "
    "de 1,2 mm de espessura; anel intermediário branco de contraste (9,2 mm); e pictograma vetorial oficial de posto de fiscalização/posto avançado "
    "('ranger-station') em branco puro (7,0 mm), consagrando a identidade visual oficial do órgão no mapa."
)

add_item_lista(
    "g) Reestruturação Temática e Categorização da Biodiversidade (Fauna vs. Flora)",
    "Identificou-se que a camada anteriormente denominada 'Vegetação e Flora (Árvores Matrizes)' agregava de forma inadequada "
    "feições faunísticas e pesqueiras de alta relevância sob símbolos arbóreos. A base foi reestruturada em 5 classes macro: "
    "1) Fauna Aquática e Pesca (pontos de avistamento de botos, áreas de piracema de curimatã, berçários de pirarucu e peixe-boi e piscicultura); "
    "2) Quelônios e Répteis (rotas migratórias, potenciais tabuleiros e ninhos de pitiú/tracajá); "
    "3) Flora e Extrativismo (árvores matrizes de jatobá, seringais nativos e matas comunitárias); "
    "4) Santuários e Refúgios Silvestres; e "
    "5) Usos Tradicionais e Manejo. "
    "No SIG, aplicou-se renderizador categorizado ('categorizedSymbol') com pictogramas SVG zoológicos e botânicos específicos para cada tema."
)

# 5. Resultados
add_secao("5. Resultados e Balanço Quantitativo da Limpeza")
add_paragrafo(
    "A execução dos algoritmos de depuração promoveu uma redução líquida de 99 registros redundantes na base territorial, "
    "passando de 746 pontos brutos consolidados para 647 feições geográficas unívocas, plenamente auditadas "
    "e sem sobreposições espúrias."
)

# Tabela 1: Balanço por Camada
p_t1 = doc.add_paragraph()
p_t1.paragraph_format.space_before = Pt(6)
p_t1.paragraph_format.space_after = Pt(2)
r_t1 = p_t1.add_run("Tabela 1 – Balanço Quantitativo de Depuração e Deduplicação por Camada Temática")
r_t1.font.name = "Arial"
r_t1.font.size = Pt(10)
r_t1.font.bold = True

tab1 = doc.add_table(rows=1, cols=4)
tab1.style = 'Table Grid'
tab1.alignment = WD_TABLE_ALIGNMENT.CENTER

hdr1 = tab1.rows[0].cells
headers1 = ["Camada Temática de Campo", "Pontos Originais", "Pontos Homologados", "Registros Depurados"]
for i, h in enumerate(headers1):
    hdr1[i].text = h
    set_cell_background(hdr1[i], "E6EDE8")
    set_cell_margins(hdr1[i], top=120, bottom=120, left=140, right=140)
    for p in hdr1[i].paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i > 0 else WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = "Arial"
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(27, 54, 38)

dados_tab1 = [
    ("01. Moradores e Comunidades Ribeirinhas", "282", "239", "-43 duplicatas"),
    ("02. Apoio de Pesca e Ranchos Sazonais", "89", "71", "-18 duplicatas"),
    ("03. Áreas de Desova (Quelônios e Peixes)", "22", "18", "-4 duplicatas"),
    ("04. Hidrografia (Rios, Furos e Igarapés)", "134", "129", "-5 duplicatas"),
    ("05. Ilhas e Praias (Bancos de Areia)", "78", "73", "-5 duplicatas"),
    ("06. Infraestrutura e Equipamentos Públicos", "19", "16", "-3 duplicatas"),
    ("07. Marcos e Pontos de Referência Locais", "16", "15", "-1 duplicata"),
    ("08. Biodiversidade: Fauna, Flora e Recursos Naturais", "50", "44", "-6 duplicatas"),
    ("09. Ocorrências e Impactos Ambientais", "7", "7", "0 (inalterado)"),
    ("10. Trajetos e Acessos Fluviais e Trilhas", "49", "35", "-14 (4 almoços + 10 passadas)"),
    ("TOTAL CONSOLIDADO DE CAMPO", "746", "647", "-99 registros eliminados")
]

for row_data in dados_tab1:
    row = tab1.add_row()
    is_total = "TOTAL" in row_data[0]
    for i, val in enumerate(row_data):
        cell = row.cells[i]
        cell.text = val
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        if is_total:
            set_cell_background(cell, "F2F5F3")
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i > 0 else WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Arial"
                run.font.size = Pt(9.0)
                if is_total:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(27, 54, 38)

p_esp = doc.add_paragraph()
p_esp.paragraph_format.space_after = Pt(6)

# Tabela 2: Exemplos de Unificação
p_t2 = doc.add_paragraph()
p_t2.paragraph_format.space_before = Pt(4)
p_t2.paragraph_format.space_after = Pt(2)
r_t2 = p_t2.add_run("Tabela 2 – Amostragem de Feições Duplicadas Unificadas com Base na Qualidade Toponímica")
r_t2.font.name = "Arial"
r_t2.font.size = Pt(10)
r_t2.font.bold = True

tab2 = doc.add_table(rows=1, cols=4)
tab2.style = 'Table Grid'
tab2.alignment = WD_TABLE_ALIGNMENT.CENTER

hdr2 = tab2.rows[0].cells
headers2 = ["Distância", "Feição Homologada (Preservada)", "Feição Redundante (Expurgada)", "Ação Técnica Aplicada"]
for i, h in enumerate(headers2):
    hdr2[i].text = h
    set_cell_background(hdr2[i], "E6EDE8")
    set_cell_margins(hdr2[i], top=120, bottom=120, left=140, right=140)
    for p in hdr2[i].paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = "Arial"
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(27, 54, 38)

dados_tab2 = [
    ("0,0 m", "ID 257: Joelma do Socorro Firmino da Rocha", "ID 10: Joelma do Socorro", "Preservação de patronímico completo"),
    ("0,0 m", "ID 7: Rancho / Morador (Bil rancho)", "ID 396: Rancho do Bil", "Unificação de duplicata exata de coordenada"),
    ("0,0 m", "ID 42: Rancho (Desconhecido)", "ID 389: Rancho desconhecido", "Eliminação de dupla inserção de campo"),
    ("2,0 m", "ID 608: Entrada da casa do seu Waldevir", "ID 609: Entrada se Waldevir", "Correção ortográfica e eliminação de duplicata"),
    ("8,8 m", "ID 16: Choinha", "ID 149: Choinha", "Fusão de passagem múltipla da mesma moradia"),
    ("8,9 m", "ID 110: Base Ideflor-bio", "ID 109: Base Ideflor", "Padronização institucional da Sede Avançada"),
    ("11,4 m", "ID 40: Rancho / Morador (Maria Duarte)", "ID 350: Rancho Maria Duarte", "Fusão de rancho cadastrado por equipes distintas"),
    ("12,6 m", "ID 52: Chica Catiara", "ID 148: Chica Catiara", "Unificação de feição idêntica em bordo de calha"),
    ("13,6 m", "ID 78: Naldo / Valdenir Caetano da Silva", "ID 449: Valdenir Caetano da Silva", "Agregação de identificação toponímica expandida"),
    ("14,9 m", "ID 124: Bito - Benedito Ferreira de Souza", "ID 13: Bito", "Substituição de apelido por qualificação formal"),
    ("24,7 m", "ID 28: Moradores (Prof. Beninha / Venceslau)", "ID 408: Rancho do prof. Benhinha", "Consolidação de residência principal e rancho contíguo")
]

for row_data in dados_tab2:
    row = tab2.add_row()
    for i, val in enumerate(row_data):
        cell = row.cells[i]
        cell.text = val
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Arial"
                run.font.size = Pt(8.5)

# 6. Conclusão e Encaminhamento
add_secao("6. Conclusão e Encaminhamentos")
add_paragrafo(
    "Os trabalhos de tratamento cartográfico executados pelo Núcleo de Geotecnologias asseguram a integridade topológica, "
    "a precisão métrica e a clareza temática do acervo fundiário e de recursos naturais do REVIS Tabuleiro do Embaubal e da RDS Vitória de Souzel. "
    "A eliminação das 134 feições espúrias e redundantes outorga confiabilidade estatística aos diagnósticos do Plano de Gestão, "
    "evitando contagens inflacionadas de populações ribeirinhas ou estruturas operacionais."
)
add_paragrafo(
    "Informa-se que as pranchas cartográficas institucionais oficiais em formato A1 seguem anexas ao processo eletrônico "
    "em formato PDF vetorial, conforme preconizado pelos padrões do Sistema de Processo Eletrônico (PAe/SEI). "
    "As camadas geoespaciais higienizadas nos formatos abertos GeoJSON, GeoPackage (.gpkg) e Shapefile (.shp), "
    "juntamente com o projeto cartográfico consolidado ('tabuleiro_do_embaubal_e_vitoria_souzel.qgz'), foram arquivados no repositório "
    "institucional do NGEO e encontram-se disponíveis para compartilhamento via correio eletrônico institucional (e-mail)."
)

# 7. Referências
add_secao("7. Referências")
add_item_lista(
    "BRASIL. Instituto Brasileiro de Geografia e Estatística – IBGE",
    "Bases Cartográficas Contínuas do Brasil, malha municipal e malha hidrográfica de referência. Rio de Janeiro: IBGE, 2022."
)
add_item_lista(
    "PARÁ (Estado). Decreto Estadual nº 1.566, de 21 de junho de 2016",
    "Cria o Refúgio de Vida Silvestre Tabuleiro do Embaubal no Município de Senador José Porfírio. Diário Oficial do Estado do Pará, Belém, 2016."
)
add_item_lista(
    "PARÁ (Estado). Decreto Estadual nº 1.567, de 21 de junho de 2016",
    "Cria a Reserva de Desenvolvimento Sustentável Vitória de Souzel nos Municípios de Senador José Porfírio e Porto de Moz. Diário Oficial do Estado do Pará, Belém, 2016."
)
add_item_lista(
    "IDEFLOR-BIO. Instituto de Desenvolvimento Florestal e da Biodiversidade do Estado do Pará",
    "Levantamento e Cadastramento de Campo de Populações Tradicionais e Recursos Pesqueiros no Baixo Xingu. Relatórios de Campo DGMUC/NGEO, 2025/2026."
)

# Assinatura Oficial
p_ass = doc.add_paragraph()
p_ass.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ass.paragraph_format.space_before = Pt(36)
p_ass.paragraph_format.space_after = Pt(2)
p_ass.paragraph_format.line_spacing = 1.15

r_nome = p_ass.add_run("SAMUEL DA COSTA DOS SANTOS\n")
r_nome.font.name = "Arial"
r_nome.font.size = Pt(12)
r_nome.font.bold = True
r_nome.font.color.rgb = RGBColor(27, 54, 38)

r_cargo = p_ass.add_run("Coordenador do Núcleo de Geotecnologias – NGEO\n")
r_cargo.font.name = "Arial"
r_cargo.font.size = Pt(11)
r_cargo.font.bold = True

r_inst = p_ass.add_run("Instituto de Desenvolvimento Florestal e da Biodiversidade do Estado do Pará – IDEFLOR-Bio")
r_inst.font.name = "Arial"
r_inst.font.size = Pt(10.5)

# Salva documento nos dois destinos
doc.save(OUTPUT_PATH)
doc.save(OUTPUT_ROOT)

print(f"\n[SUCESSO] Relatório Técnico Oficial gerado em:")
print(f"  -> {OUTPUT_PATH}")
print(f"  -> {OUTPUT_ROOT}")
