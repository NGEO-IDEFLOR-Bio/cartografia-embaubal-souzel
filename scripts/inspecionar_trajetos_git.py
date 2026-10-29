import subprocess, json

out = subprocess.check_output(['git', 'show', '1c53a73:camadas/10_trajetos_e_acessos.geojson']).decode('utf-8')
data = json.loads(out)
print(f"Total features in git commit 1c53a73: {len(data['features'])}")

for i, f in enumerate(data['features']):
    p = f['properties']
    coords = f['geometry']['coordinates']
    print(f"{i:2d}: ID {p.get('id')} | nome: '{p.get('nome')}' | alt: '{p.get('nome_alternativo')}' | obs: '{p.get('observacoes')}' | coords: {coords}")
