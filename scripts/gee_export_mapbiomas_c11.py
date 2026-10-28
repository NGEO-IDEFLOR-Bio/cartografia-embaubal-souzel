"""
Script Google Earth Engine (Python API) - Coleção 11 MapBiomas
Asset de UCs: 'projects/ee-samuelsantosambientalcourse/assets/00_ucs_alvo_embaubal_souzel'
"""

import ee

def exportar_mapbiomas():
    # Inicializa o Earth Engine associando ao projeto do usuário
    ee.Initialize(project='ee-samuelsantosambientalcourse')
    
    # Carrega o asset das UCs do usuário
    ucs = ee.FeatureCollection('projects/ee-samuelsantosambientalcourse/assets/00_ucs_alvo_embaubal_souzel')
    geom_ucs = ucs.geometry()
    roi_buffer = geom_ucs.buffer(5000)
    
    asset_id = 'projects/mapbiomas-public/assets/brazil/lulc/collection11/mapbiomas_brazil_collection11_coverage_v3'
    mapbiomas = ee.Image(asset_id)
    
    # 1. Exportar ano mais recente (2024) com Buffer
    img_2024_buffer = mapbiomas.select('classification_2024').clip(roi_buffer)
    task1 = ee.batch.Export.image.toDrive(
        image=img_2024_buffer,
        description='MapBiomas_Col11_2024_Buffer5km',
        folder='GEE_MapBiomas_Embaubal',
        fileNamePrefix='mapbiomas_c11_2024_buffer5km',
        region=roi_buffer,
        scale=30,
        crs='EPSG:4674',
        maxPixels=1e9,
        fileFormat='GeoTIFF'
    )
    task1.start()
    print("Tarefa 2024 (Buffer) iniciada! ID:", task1.id)

    # 2. Exportar ano mais recente (2024) recorte exato das UCs
    img_2024_exato = mapbiomas.select('classification_2024').clip(geom_ucs)
    task2 = ee.batch.Export.image.toDrive(
        image=img_2024_exato,
        description='MapBiomas_Col11_2024_LimitesExatos',
        folder='GEE_MapBiomas_Embaubal',
        fileNamePrefix='mapbiomas_c11_2024_limites_exatos',
        region=geom_ucs,
        scale=30,
        crs='EPSG:4674',
        maxPixels=1e9,
        fileFormat='GeoTIFF'
    )
    task2.start()
    print("Tarefa 2024 (Limites Exatos) iniciada! ID:", task2.id)

    # 3. Exportar série temporal de anos chave
    anos = ['classification_1985', 'classification_1995', 'classification_2005', 'classification_2015', 'classification_2024']
    img_temporal = mapbiomas.select(anos).clip(roi_buffer)
    task3 = ee.batch.Export.image.toDrive(
        image=img_temporal,
        description='MapBiomas_Col11_Temporal_1985_2024',
        folder='GEE_MapBiomas_Embaubal',
        fileNamePrefix='mapbiomas_c11_temporal_1985_2024',
        region=roi_buffer,
        scale=30,
        crs='EPSG:4674',
        maxPixels=1e9,
        fileFormat='GeoTIFF'
    )
    task3.start()
    print("Tarefa Temporal (1985-2024) iniciada! ID:", task3.id)

if __name__ == '__main__':
    try:
        exportar_mapbiomas()
    except Exception as e:
        print("Erro ao executar script EE:", e)
