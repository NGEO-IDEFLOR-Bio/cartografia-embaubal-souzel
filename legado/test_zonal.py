from qgis.core import (
    QgsApplication,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsGeometry,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject
)
import json

QgsApplication.setPrefixPath("C:/Program Files/QGIS 4.2.3/apps/qgis", True)
qgs = QgsApplication([], False)
qgs.initQgis()

vec_path = "camadas/00_ucs_alvo_embaubal_souzel.geojson"
rast_path = "camadas/raster/mapbiomas_c11_temporal_1985_2024.tif"

vec = QgsVectorLayer(vec_path, "ucs", "ogr")
rast = QgsRasterLayer(rast_path, "temporal")

print("Vector valid:", vec.isValid(), "Features:", vec.featureCount())
print("Raster valid:", rast.isValid(), "Bands:", rast.bandCount())

for f in vec.getFeatures():
    print("UC Feature:", f["Nome"], "| Categoria:", f["Categoria"])

qgs.exitQgis()
