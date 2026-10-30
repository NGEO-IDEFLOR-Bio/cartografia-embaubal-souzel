# -*- coding: utf-8 -*-
import docx, glob

p = glob.glob('relatorios/*Relat*rio.docx')[0]
doc = docx.Document(p)

ajustes = 0
for i, para in enumerate(doc.paragraphs):
    txt = para.text
    # 1. Typos de decreto
    if "Decreto Estadual nº 1.566, de 17 de junho de 2016" in txt and ("As duas Unidades" in txt or "as duas Unidades" in txt):
        para.text = txt.replace(
            "pelo Decreto Estadual nº 1.566, de 17 de junho de 2016",
            "pelos Decretos Estaduais nº 1.566 e nº 1.567, de 17 de junho de 2016"
        )
        print(f"[OK] Ajuste Decreto no parágrafo {i}")
        ajustes += 1
    # 2. Typos 'a RDS' no início de frase
    if txt.startswith("a RDS Vitória de Souzel"):
        para.text = "N" + txt
        print(f"[OK] Ajuste 'Na RDS' no parágrafo {i}")
        ajustes += 1
    # 3. Typos 9Sankey
    if "9Sankey" in txt:
        para.text = txt.replace("9Sankey", "(Sankey")
        print(f"[OK] Ajuste '(Sankey' no parágrafo {i}")
        ajustes += 1

doc.save(p)
print(f"Total de micro-ajustes aplicados em {p}: {ajustes}")
