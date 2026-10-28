/**
 * =========================================================================================
 * GOOGLE EARTH ENGINE (GEE) - MAPBIOMAS COLEÇÃO 11 (1985 - 2024)
 * UNIDADES DE CONSERVAÇÃO:
 * - REVIS Tabuleiro do Embaubal
 * - RDS Vitória de Souzel
 * 
 * Asset importado pelo usuário:
 * 'projects/ee-samuelsantosambientalcourse/assets/00_ucs_alvo_embaubal_souzel'
 * =========================================================================================
 */

// 1. CARREGAR AS UNIDADES DE CONSERVAÇÃO (ASSET DO USUÁRIO)
var ucs = ee.FeatureCollection('projects/ee-samuelsantosambientalcourse/assets/00_ucs_alvo_embaubal_souzel');

// Geometria das UCs combinadas e com buffer de 5 km para contexto cartográfico
var geomUcs = ucs.geometry();
var roiBuffer = geomUcs.buffer(5000);

Map.centerObject(ucs, 11);
Map.setOptions('HYBRID');

// 2. ASSET OFICIAL MAPBIOMAS COLEÇÃO 11
var assetMapBiomas = 'projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_coverage_v3';
var mapbiomas = ee.Image(assetMapBiomas);

// 3. TABELA OFICIAL DE CLASSES E CORES MAPBIOMAS COLEÇÃO 11
var legendDict = [
  {id: 1,  name: '1. Floresta', color: '#1f8d49'},
  {id: 3,  name: '1.1. Formação Florestal', color: '#1f8d49'},
  {id: 6,  name: '1.2. Floresta Alagável', color: '#007785'},
  {id: 4,  name: '1.3. Formação Savânica', color: '#7dc975'},
  {id: 7,  name: '1.4. Savana Alagada (beta)', color: '#228c70'},
  {id: 5,  name: '1.5. Mangue', color: '#04381d'},
  {id: 49, name: '1.6. Restinga Arbórea', color: '#02d659'},
  {id: 10, name: '2. Veg. Herbácea e Arbustiva', color: '#d6bc74'},
  {id: 12, name: '2.1. Formação Campestre', color: '#d6bc74'},
  {id: 77, name: '2.2. Formação Herbáceo Arbustiva', color: '#86b074'},
  {id: 11, name: '2.3. Campo Alagado e Área Pantanosa', color: '#519799'},
  {id: 84, name: '2.4. Marisma (beta)', color: '#81dbbf'},
  {id: 50, name: '2.5. Restinga Herbácea ou Arbustiva', color: '#ffaa5f'},
  {id: 32, name: '2.6. Apicum', color: '#fc8114'},
  {id: 29, name: '2.7. Afloramento Rochoso', color: '#ad5100'},
  {id: 14, name: '3. Agropecuária', color: '#ffefc3'},
  {id: 15, name: '3.1. Pastagem', color: '#edde8e'},
  {id: 18, name: '3.2. Agricultura', color: '#E974ED'},
  {id: 19, name: '3.2.1. Lavoura Temporária', color: '#C27BA0'},
  {id: 39, name: '3.2.1.1. Soja', color: '#f5b3c8'},
  {id: 20, name: '3.2.1.2. Cana', color: '#db7093'},
  {id: 40, name: '3.2.1.3. Arroz', color: '#c71585'},
  {id: 62, name: '3.2.1.4. Algodão (beta)', color: '#ff69b4'},
  {id: 41, name: '3.2.1.5. Outras Lavouras Temporárias', color: '#f54ca9'},
  {id: 36, name: '3.2.2. Lavoura Perene', color: '#d082de'},
  {id: 46, name: '3.2.2.1. Café', color: '#d68fe2'},
  {id: 47, name: '3.2.2.2. Citrus', color: '#9932cc'},
  {id: 35, name: '3.2.2.3. Dendê', color: '#9065d0'},
  {id: 48, name: '3.2.2.4. Outras Lavouras Perenes', color: '#e6ccff'},
  {id: 9,  name: '3.3. Silvicultura', color: '#7a5900'},
  {id: 21, name: '3.4. Mosaico de Usos', color: '#ffefc3'},
  {id: 22, name: '4. Área não Vegetada', color: '#d4271e'},
  {id: 23, name: '4.1. Praia, Duna e Areal', color: '#ffa07a'},
  {id: 24, name: '4.2. Área Urbanizada', color: '#d4271e'},
  {id: 30, name: '4.3. Mineração', color: '#9c0027'},
  {id: 75, name: '4.4. Usina Fotovoltaica', color: '#757272'},
  {id: 91, name: '4.5. Parque Eólico (beta)', color: '#403d3e'},
  {id: 25, name: '4.6. Outras Áreas não Vegetadas', color: '#db4d4f'},
  {id: 26, name: '5. Corpo D\'Água', color: '#2532e4'},
  {id: 33, name: '5.1. Rio, Lago e Oceano', color: '#2532e4'},
  {id: 31, name: '5.2. Aquicultura', color: '#091077'},
  {id: 27, name: 'Não Observado', color: '#ffffff'}
];

var classIds = legendDict.map(function(item) { return item.id; });
var classColors = legendDict.map(function(item) { return item.color; });

var indices = [];
for (var i = 0; i < classIds.length; i++) { indices.push(i); }

function styleMapBiomas(imageBand) {
  return imageBand.remap(classIds, indices).visualize({
    min: 0,
    max: indices.length - 1,
    palette: classColors
  });
}

// 4. CAMADAS TEMPORAIS NO MAPA
var lulc2024 = mapbiomas.select('classification_2024').clip(roiBuffer);
var lulc2015 = mapbiomas.select('classification_2015').clip(roiBuffer);
var lulc2005 = mapbiomas.select('classification_2005').clip(roiBuffer);
var lulc1995 = mapbiomas.select('classification_1995').clip(roiBuffer);
var lulc1985 = mapbiomas.select('classification_1985').clip(roiBuffer);

// Adicionar camadas históricas (desmarcadas por padrão)
Map.addLayer(styleMapBiomas(lulc1985), {}, 'MapBiomas Col 11 - 1985', false);
Map.addLayer(styleMapBiomas(lulc1995), {}, 'MapBiomas Col 11 - 1995', false);
Map.addLayer(styleMapBiomas(lulc2005), {}, 'MapBiomas Col 11 - 2005', false);
Map.addLayer(styleMapBiomas(lulc2015), {}, 'MapBiomas Col 11 - 2015', false);
Map.addLayer(styleMapBiomas(lulc2024), {}, 'MapBiomas Col 11 - 2024 (Recente)', true);

// Limites das UCs por cima
Map.addLayer(ucs.style({color: 'ffff00', fillColor: '00000000', width: 2.5}), {}, 'Limites REVIS e RDS (Asset)');
Map.addLayer(ee.FeatureCollection([ee.Feature(roiBuffer)]).style({color: 'ff0000', fillColor: '00000000', width: 1.5, lineType: 'dashed'}), {}, 'Buffer 5km de Exportação', false);

// 5. CÁLCULO DE ESTATÍSTICAS DE ÁREA (HECTARES) POR UNIDADE DE CONSERVAÇÃO
var pixelAreaHa = ee.Image.pixelArea().divide(10000);
var area2024 = pixelAreaHa.addBands(mapbiomas.select('classification_2024'));

// Calcular para cada UC individualmente (REVIS e RDS)
var statsPorUc = ucs.map(function(feat) {
  var nome = feat.get('Nome');
  var stats = area2024.reduceRegion({
    reducer: ee.Reducer.sum().group({
      groupField: 1,
      groupName: 'classe_id'
    }),
    geometry: feat.geometry(),
    scale: 30,
    maxPixels: 1e9
  });
  return feat.set('estatisticas_2024', stats.get('groups'));
});

print('========================================================================');
print('1. ESTATÍSTICAS DE ÁREA (HA) POR UC - 2024 (REVIS e RDS):');
print(statsPorUc.select(['Nome', 'Categoria', 'estatisticas_2024']));
print('========================================================================');

// 6. EXPORTAÇÕES PARA O GOOGLE DRIVE

// A. GeoTIFF com Buffer de 5km (Ideal para o mapa de localização e enquadramento A1)
Export.image.toDrive({
  image: lulc2024,
  description: 'MapBiomas_Col11_2024_Buffer5km',
  folder: 'GEE_MapBiomas_Embaubal',
  fileNamePrefix: 'mapbiomas_c11_2024_buffer5km',
  region: roiBuffer,
  scale: 30,
  crs: 'EPSG:4674', // SIRGAS 2000 Geográfico
  maxPixels: 1e9,
  fileFormat: 'GeoTIFF'
});

// B. GeoTIFF Recortado Exatamente nos Limites das UCs (Máscara precisa)
var lulc2024_exato = mapbiomas.select('classification_2024').clip(geomUcs);
Export.image.toDrive({
  image: lulc2024_exato,
  description: 'MapBiomas_Col11_2024_LimitesExatos_UCs',
  folder: 'GEE_MapBiomas_Embaubal',
  fileNamePrefix: 'mapbiomas_c11_2024_limites_exatos_ucs',
  region: geomUcs,
  scale: 30,
  crs: 'EPSG:4674',
  maxPixels: 1e9,
  fileFormat: 'GeoTIFF'
});

// C. Série Temporal Multibandas (1985, 1995, 2005, 2015, 2024) para os Mapas de Análise Temporal
var temporalStack = mapbiomas.select([
  'classification_1985',
  'classification_1995',
  'classification_2005',
  'classification_2015',
  'classification_2024'
]).clip(roiBuffer);

Export.image.toDrive({
  image: temporalStack,
  description: 'MapBiomas_Col11_Temporal_1985_2024',
  folder: 'GEE_MapBiomas_Embaubal',
  fileNamePrefix: 'mapbiomas_c11_temporal_1985_2024',
  region: roiBuffer,
  scale: 30,
  crs: 'EPSG:4674',
  maxPixels: 1e9,
  fileFormat: 'GeoTIFF'
});

print('-> Tarefas criadas na aba "Tasks" à direita. Clique em RUN em cada uma para exportar ao Drive!');
