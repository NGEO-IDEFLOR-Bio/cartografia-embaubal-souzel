# -*- coding: utf-8 -*-
import geopandas as gpd

gdf = gpd.read_file('camadas/08_vegetacao_e_flora.geojson')

CLASSIFICACAO = {
    # Fauna Aquática e Ictiofauna
    586: {'grupo': 'Fauna Aquática e Ictiofauna', 'tipo': 'Área de Piracema', 'nome': 'Área de Piracema (Curimatã)', 'icone': 'fish'},
    581: {'grupo': 'Fauna Aquática e Ictiofauna', 'tipo': 'Avistamento de Botos', 'nome': 'Ponto de Avistamento de Botos', 'icone': 'dolphin'},
    587: {'grupo': 'Aquicultura e Manejo Tradicional', 'tipo': 'Piscicultura', 'nome': 'Área de Piscicultura (Tanque-Rede)', 'icone': 'net'},
    121: {'grupo': 'Fauna Aquática e Ictiofauna', 'tipo': 'Berçário Aquático', 'nome': 'Berçário Natural de Peixes', 'icone': 'fish'},
    122: {'grupo': 'Fauna Aquática e Ictiofauna', 'tipo': 'Berçário Aquático', 'nome': 'Berçário de Pirarucu e Peixe-Boi', 'icone': 'fish'},
    123: {'grupo': 'Fauna Aquática e Ictiofauna', 'tipo': 'Berçário Aquático', 'nome': 'Berçário de Pirarucu', 'icone': 'fish'},
    126: {'grupo': 'Fauna Aquática e Ictiofauna', 'tipo': 'Mamíferos Aquáticos', 'nome': 'Boiador de Peixe-Boi', 'icone': 'manatee'},
    304: {'grupo': 'Fauna Aquática e Ictiofauna', 'tipo': 'Alimentação de Peixe-Boi', 'nome': 'Área de Alimentação de Peixe-Boi (Pastagem)', 'icone': 'manatee'},
    305: {'grupo': 'Fauna Aquática e Ictiofauna', 'tipo': 'Alimentação de Peixe-Boi', 'nome': 'Área de Alimentação de Peixe-Boi', 'icone': 'manatee'},
    567: {'grupo': 'Fauna Aquática e Ictiofauna', 'tipo': 'Mamíferos Aquáticos', 'nome': 'Área de Ocorrência de Peixe-Boi', 'icone': 'manatee'},

    # Quelônios e Répteis
    125: {'grupo': 'Quelônios e Répteis', 'tipo': 'Boiadeiro de Quelônios', 'nome': 'Boiadeiro de Tartarugas', 'icone': 'turtle'},
    153: {'grupo': 'Quelônios e Répteis', 'tipo': 'Concentração de Quelônios', 'nome': 'Área de Concentração de Tartarugas', 'icone': 'turtle'},
    154: {'grupo': 'Quelônios e Répteis', 'tipo': 'Concentração de Quelônios', 'nome': 'Área de Concentração de Tartarugas', 'icone': 'turtle'},
    155: {'grupo': 'Quelônios e Répteis', 'tipo': 'Concentração de Quelônios', 'nome': 'Área de Concentração de Tartarugas', 'icone': 'turtle'},
    294: {'grupo': 'Quelônios e Répteis', 'tipo': 'Ninho de Quelônios', 'nome': 'Ninho de Pitiú', 'icone': 'turtle'},
    295: {'grupo': 'Quelônios e Répteis', 'tipo': 'Ninho de Quelônios', 'nome': 'Ninho de Pitiú', 'icone': 'turtle'},
    325: {'grupo': 'Quelônios e Répteis', 'tipo': 'Tabuleiro de Desova', 'nome': 'Potencial Tabuleiro de Tartaruga', 'icone': 'turtle'},
    432: {'grupo': 'Quelônios e Répteis', 'tipo': 'Rota Migratória', 'nome': 'Rota de Migração de Tartarugas', 'icone': 'turtle'},
    470: {'grupo': 'Quelônios e Répteis', 'tipo': 'Concentração de Quelônios', 'nome': 'Área de Abundância de Tracajá e Tartaruga', 'icone': 'turtle'},
    500: {'grupo': 'Quelônios e Répteis', 'tipo': 'Ocorrência de Quelônios', 'nome': 'Lago do Palhal (Ocorrência de Tracajás)', 'icone': 'turtle'},
    412: {'grupo': 'Quelônios e Répteis', 'tipo': 'Répteis', 'nome': 'Sítio de Reprodução de Jacaré', 'icone': 'reptile'},

    # Santuários e Refúgios de Fauna
    434: {'grupo': 'Santuários e Refúgios de Fauna', 'tipo': 'Santuário de Animais', 'nome': 'Santuário de Fauna Silvestre', 'icone': 'sanctuary'},
    435: {'grupo': 'Santuários e Refúgios de Fauna', 'tipo': 'Santuário Multiespécie', 'nome': 'Santuário de Tartarugas, Peixe-Boi e Pirarucu', 'icone': 'sanctuary'},
    72:  {'grupo': 'Fauna Terrestre', 'tipo': 'Mamíferos Terrestres', 'nome': 'Ponto de Avistamento de Cutia', 'icone': 'mammal'},

    # Flora Nativa e Extrativismo
    21:  {'grupo': 'Flora e Extrativismo', 'tipo': 'Seringal', 'nome': 'Seringal Nativo', 'icone': 'tree'},
    26:  {'grupo': 'Flora e Vegetação', 'tipo': 'Vegetação Natural', 'nome': 'Formação Arbórea Seca', 'icone': 'tree'},
    36:  {'grupo': 'Flora e Vegetação', 'tipo': 'Mata Nativa', 'nome': 'Área de Floresta Nativa', 'icone': 'tree'},
    69:  {'grupo': 'Flora e Extrativismo', 'tipo': 'Seringueira Matriz', 'nome': 'Seringueira Matriz (Lanhada)', 'icone': 'tree'},
    105: {'grupo': 'Flora e Vegetação', 'tipo': 'Campos Naturais', 'nome': 'Formação de Campos Naturais', 'icone': 'grass'},
    310: {'grupo': 'Flora e Frutíferas', 'tipo': 'Frutífera Nativa', 'nome': 'Ocorrência de Pitanguinha', 'icone': 'tree'},
    311: {'grupo': 'Uso Agroflorestal', 'tipo': 'Cacaual', 'nome': 'Área de Plantio de Cacau', 'icone': 'tree'},
    453: {'grupo': 'Flora e Vegetação', 'tipo': 'Embaubal Nativo', 'nome': 'Formação Típica de Embaubal', 'icone': 'tree'},
    471: {'grupo': 'Flora e Extrativismo', 'tipo': 'Seringal', 'nome': 'Ocorrência de Seringueiras', 'icone': 'tree'},
    478: {'grupo': 'Flora e Extrativismo', 'tipo': 'Seringal Histórico', 'nome': 'Antigo Seringal', 'icone': 'tree'},
    499: {'grupo': 'Flora e Árvores Matrizes', 'tipo': 'Árvore Matriz', 'nome': 'Jatobá Matriz', 'icone': 'tree'},
    555: {'grupo': 'Flora e Árvores Matrizes', 'tipo': 'Árvore Matriz', 'nome': 'Seringueira Matriz (Lanhada)', 'icone': 'tree'},
    590: {'grupo': 'Conservação Comunitária', 'tipo': 'Reserva Comunitária', 'nome': 'Mata Preservada da Comunidade', 'icone': 'tree'},

    # Atividades Agropecuárias
    152: {'grupo': 'Atividades Agropecuárias', 'tipo': 'Pecuária Bovina', 'nome': 'Área de Concentração de Gado', 'icone': 'livestock'},
    585: {'grupo': 'Atividades Agropecuárias', 'tipo': 'Pecuária Bovina', 'nome': 'Área de Manejo de Gado no Verão', 'icone': 'livestock'},
    589: {'grupo': 'Atividades Agropecuárias', 'tipo': 'Pecuária Bubalina', 'nome': 'Área com Presença de Búfalos', 'icone': 'livestock'},

    # Acidentes Geográficos / Hidrografia
    479: {'grupo': 'Hidrografia e Referência Local', 'tipo': 'Canal Hídrico', 'nome': 'Braço do Meio (Referência Local)', 'icone': 'water'},
    480: {'grupo': 'Hidrografia e Referência Local', 'tipo': 'Canal Hídrico', 'nome': 'Braço do Meio (Extremidade)', 'icone': 'water'},
    487: {'grupo': 'Hidrografia e Intervenção', 'tipo': 'Hidrovia', 'nome': 'Canal de Dragagem', 'icone': 'water'},
    566: {'grupo': 'Hidrografia e Manejo Hídrico', 'tipo': 'Tapagem', 'nome': 'Tapagem Divisória de Lagos', 'icone': 'water'}
}

print(f"Total classificados: {len(CLASSIFICACAO)} de {len(gdf)} feições.")
for nid in sorted(gdf['id'].unique()):
    if nid not in CLASSIFICACAO:
        print(f"[!] ID {nid} não está no dicionário!")

# Resumo por grupo
from collections import Counter
grupos = [v['grupo'] for v in CLASSIFICACAO.values()]
for g, c in Counter(grupos).most_common():
    print(f"  • {g}: {c} feições")
