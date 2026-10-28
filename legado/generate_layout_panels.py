import os
import subprocess
from PIL import Image

output_dir = "paineis_tematicos_graficos"
os.makedirs(output_dir, exist_ok=True)

html_files = [
    ("01_limites_e_unidades_conservacao.html", "01_limites_e_unidades_conservacao.png"),
    ("02_gestao_e_infraestrutura.html", "02_gestao_e_infraestrutura.png"),
    ("03_biodiversidade_e_protecao_ambiental.html", "03_biodiversidade_e_protecao_ambiental.png"),
    ("04_comunidades_e_uso_tradicional.html", "04_comunidades_e_uso_tradicional.png"),
    ("05_geografia_e_hidrografia.html", "05_geografia_e_hidrografia.png"),
]

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
base_dir = os.path.abspath(".")

for html_name, png_name in html_files:
    html_path = os.path.join(base_dir, "paineis_tematicos_html", html_name)
    temp_png = os.path.join(base_dir, output_dir, "temp_" + png_name)
    final_png = os.path.join(base_dir, output_dir, png_name)
    
    # 136.382 mm * 96 / 25.4 = 515.46 px
    # 186.572 mm * 96 / 25.4 = 705.15 px
    # Scale factor 3.125 gives exact 300 DPI (1610.8 x 2203.6 px)
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--force-device-scale-factor=3.125",
        f"--screenshot={temp_png}",
        "--window-size=515,705",
        html_path
    ]
    
    print(f"Rendering: {html_name} -> {png_name}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(temp_png):
        # Open and save with 300 DPI metadata
        im = Image.open(temp_png)
        # Ensure exact 1611 x 2204
        if im.size != (1611, 2204):
            im = im.resize((1611, 2204), Image.Resampling.LANCZOS)
        im.save(final_png, dpi=(300, 300))
        os.remove(temp_png)
        print(f"  Saved: {final_png} ({im.size[0]}x{im.size[1]} px @ 300 DPI)")
    else:
        print(f"  Error rendering {html_name}: {res.stderr}")

print("\n--- All 5 Graphic Panels Generated Successfully! ---")
