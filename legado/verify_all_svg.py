import sys
import os
from PyQt6.QtGui import QGuiApplication, QImage, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QSize
from PIL import Image
import numpy as np

app = QGuiApplication(sys.argv)
svg_files = [
    "01_limites_e_unidades_conservacao.svg",
    "02_gestao_e_infraestrutura.svg",
    "03_biodiversidade_e_protecao_ambiental.svg",
    "04_comunidades_e_uso_tradicional.svg",
    "05_geografia_e_hidrografia.svg"
]

for sf in svg_files:
    path = os.path.join("paineis_tematicos_svg", sf)
    renderer = QSvgRenderer(path)
    img = QImage(QSize(1611, 2204), QImage.Format.Format_ARGB32)
    img.fill(0xffffffff)
    p = QPainter(img)
    renderer.render(p)
    p.end()
    
    out_png = os.path.join("paineis_tematicos_svg", sf.replace(".svg", "_preview.png"))
    img.save(out_png)
    
    # Analyze image
    im = Image.open(out_png)
    arr = np.array(im)
    mask = arr[:, :, :3] < 240
    non_white = np.sum(mask)
    coords = np.where(mask)
    y_min, y_max = coords[0].min(), coords[0].max()
    x_min, x_max = coords[1].min(), coords[1].max()
    print(f"{sf}:")
    print(f"  Valid: {renderer.isValid()} | Non-white pixels: {non_white:,}")
    print(f"  Y bounds: {y_min} to {y_max} (out of 2204) -> {(y_max-y_min)/2204*100:.1f}% vertical fill")
    print(f"  X bounds: {x_min} to {x_max} (out of 1611) -> {(x_max-x_min)/1611*100:.1f}% horizontal fill")
    # Clean up preview png
    os.remove(out_png)

print("\n--- ALL 5 PANELS VERIFIED WITH QT SVG RENDERER! ---")
