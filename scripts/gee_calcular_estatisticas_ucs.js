/**
 * =========================================================================================
 * GOOGLE EARTH ENGINE (GEE) - CÁLCULO DE ESTATÍSTICAS E EXPORTAÇÃO CSV
 * UNIDADES: REVIS Tabuleiro do Embaubal e RDS Vitória de Souzel
 * ASSET: 'projects/ee-samuelsantosambientalcourse/assets/00_ucs_alvo_embaubal_souzel'
 * =========================================================================================
 * 
 * Este script calcula na nuvem do GEE:
 * 1. A área exata em HECTARES e o PERCENTUAL (%) de cada classe de uso/cobertura.
 * 2. Faz o cálculo individual para cada UC (REVIS e RDS separadamente).
 * 3. Analisa os anos da série temporal (1985, 1995, 2005, 2015, 2024).
 * 4. Imprime os gráficos e tabelas diretamente no CONSOLE do GEE.
 * 5. Cria uma tarefa na aba "Tasks" para exportar a tabela consolidada em CSV para o Google Drive!
 */

// 1. CARREGAR AS UNIDADES DE CONSERVAÇÃO
var ucs = ee.FeatureCollection('projects/ee-samuelsantosambientalcourse/assets/00_ucs_alvo_embaubal_souzel');
Map.centerObject(ucs, 11);
Map.setOptions('HYBRID');

// Desenhar limites das UCs
Map.addLayer(ucs.style({color: 'ffff00', fillColor: '00000000', width: 2.5}), {}, 'Limites das UCs');

// 2. CARREGAR ASSET MAPBIOMAS COLEÇÃO 11
var mapbiomas = ee.Image('projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_coverage_v3');

// 3. TABELA OFICIAL DE NOMES DAS CLASSES MAPBIOMAS COLEÇÃO 11
var nomesClasses = ee.Dictionary({
  '1': 'Floresta',
  '3': 'Formação Florestal',
  '4': 'Formação Savânica',
  '5': 'Mangue',
  '6': 'Floresta Alagável',
  '7': 'Savana Alagada',
  '9': 'Silvicultura',
  '10': 'Vegetação Herbácea/Arbustiva',
  '11': 'Campo Alagado e Área Pantanosa',
  '12': 'Formação Campestre',
  '14': 'Agropecuária',
  '15': 'Pastagem',
  '18': 'Agricultura',
  '19': 'Lavoura Temporária',
  '20': 'Cana',
  '21': 'Mosaico de Usos',
  '22': 'Área não Vegetada',
  '23': 'Praia, Duna e Areal',
  '24': 'Área Urbanizada',
  '25': 'Outras Áreas não Vegetadas',
  '26': 'Corpo D\'Água',
  '27': 'Não Observado',
  '29': 'Afloramento Rochoso',
  '30': 'Mineração',
  '31': 'Aquicultura',
  '32': 'Apicum',
  '33': 'Rio, Lago e Oceano',
  '35': 'Dendê',
  '36': 'Lavoura Perene',
  '39': 'Soja',
  '40': 'Arroz',
  '41': 'Outras Lavouras Temporárias',
  '46': 'Café',
  '47': 'Citrus',
  '48': 'Outras Lavouras Perenes',
  '49': 'Restinga Arbórea',
  '50': 'Restinga Herbácea',
  '62': 'Algodão',
  '75': 'Usina Fotovoltaica',
  '77': 'Formação Herbáceo Arbustiva',
  '84': 'Marisma',
  '91': 'Parque Eólico'
});

// 4. ANOS SELECIONADOS PARA A ANÁLISE TEMPORAL
var anos = [1985, 1995, 2005, 2015, 2024];

// Imagem com área de cada pixel em hectares
var pixelAreaHa = ee.Image.pixelArea().divide(10000);

// 5. PROCESSAMENTO ZONAL POR ANO E POR UNIDADE
var listaLinhas = [];

var featuresLista = ucs.toList(ucs.size());

for (var i = 0; i < 2; i++) {
  var ucFeat = ee.Feature(featuresLista.get(i));
  var nomeUc = ucFeat.get('Nome');
  var catUc = ucFeat.get('Categoria');
  var geomUc = ucFeat.geometry();

  // Iterar pelos anos da série temporal
  var linhasUc = anos.map(function(ano) {
    var bandaNome = 'classification_' + ano;
    var imgAno = mapbiomas.select(bandaNome);
    
    // Imagem combinada: Banda 0 = Área em Ha, Banda 1 = ID da Classe
    var areaEClasse = pixelAreaHa.addBands(imgAno);
    
    // Reduzir por região agrupando por ID de classe
    var reducao = areaEClasse.reduceRegion({
      reducer: ee.Reducer.sum().group({
        groupField: 1,
        groupName: 'classe_id'
      }),
      geometry: geomUc,
      scale: 30,
      maxPixels: 1e9,
      crs: 'EPSG:4674'
    });
    
    var grupos = ee.List(reducao.get('groups'));
    
    // Calcular a área total da UC naquele ano para extrair os percentuais
    var areaTotal = grupos.map(function(g) {
      return ee.Dictionary(g).getNumber('sum');
    }).reduce(ee.Reducer.sum());
    
    // Mapear cada classe para uma linha tabular
    return grupos.map(function(g) {
      var d = ee.Dictionary(g);
      var cid = ee.Number(d.get('classe_id')).format('%d');
      var areaHa = ee.Number(d.get('sum'));
      var pct = areaHa.divide(ee.Number(areaTotal)).multiply(100.0);
      var nomeCl = nomesClasses.get(cid, ee.String('Classe ').cat(cid));
      
      return ee.Feature(null, {
        'Unidade': nomeUc,
        'Categoria': catUc,
        'Ano': ano,
        'Classe_ID': ee.Number.parse(cid),
        'Classe_Nome': nomeCl,
        'Area_ha': areaHa,
        'Percentual': pct
      });
    });
  });
  
  listaLinhas.push(ee.List(linhasUc).flatten());
}

// Consolidar todas as linhas em uma FeatureCollection para exportação
var tabelaConsolidada = ee.FeatureCollection(ee.List(listaLinhas).flatten());

// 6. EXIBIÇÃO NO CONSOLE DO GEE
print('================================================================');
print('TABELA DE DADOS DE USO E COBERTURA DO SOLO (MapBiomas Col 11):');
print(tabelaConsolidada);
print('================================================================');

// 7. EXPORTAR TABELA EM CSV PARA O GOOGLE DRIVE
Export.table.toDrive({
  collection: tabelaConsolidada,
  description: 'Estatisticas_MapBiomas_C11_REVIS_RDS',
  folder: 'GEE_MapBiomas_Embaubal',
  fileNamePrefix: 'estatisticas_mapbiomas_c11_revis_rds',
  fileFormat: 'CSV',
  selectors: ['Unidade', 'Categoria', 'Ano', 'Classe_ID', 'Classe_Nome', 'Area_ha', 'Percentual']
});

print('-> Tarefa de exportação da tabela CSV criada na aba "Tasks"!');
print('-> Clique em RUN na aba Tasks para salvar o arquivo CSV no seu Google Drive.');
