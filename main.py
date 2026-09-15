import os
import requests
import fitz
from datetime import date

# Tu key la coge de GitHub Secrets. Si lo pruebas en local, ponla aqui:
API_KEY = os.environ.get("API_FOOTBALL_KEY") or "PEGA_AQUI_TU_KEY_SI_PRUEBAS_EN_LOCAL"
LEAGUE = 140 # LaLiga
SEASON = 2026 # 26/27

headers = {
    "x-apisports-key": API_KEY
}

# 1. Pedir clasificacion a API-Football
print("Pidiendo clasificacion a API-Football...")
url = f"https://v3.football.api-sports.io/standings?league={LEAGUE}&season={SEASON}"
r = requests.get(url, headers=headers, timeout=15)
data = r.json()

# Si la API falla, usa datos de respaldo
try:
    standings = data['response'][0]['league']['standings'][0]
except Exception as e:
    print(f"Error API: {e}, usando datos de respaldo")
    standings = []

equipos = []
for team in standings:
    rank = team['rank']
    t = team['team']
    all_stats = team['all']
    equipos.append({
        "POS": rank,
        "EQUIPO": t['name'],
        "PJ": all_stats['played'],
        "PTS": team['points'],
        "G": all_stats['win'],
        "E": all_stats['draw'],
        "P": all_stats['lose'],
        "GF": all_stats['goals']['for'],
        "GC": all_stats['goals']['against'],
        "DG": all_stats['goals']['for'] - all_stats['goals']['against'],
        "id": t['id'],
        "logo_url": t['logo']
    })

# Fallback por si la temporada 2026 aun no esta en tu plan free
if not equipos:
    print("Usando datos de 2023 como demo - cambia SEASON a 2023")
    equipos = [
        {"POS":1,"EQUIPO":"FC Barcelona","PJ":5,"PTS":15,"G":5,"E":0,"P":0,"GF":21,"GC":4,"DG":17,"id":529,"logo_url":"https://media.api-sports.io/football/teams/529.png"},
        #... (pon los 20 de antes si quieres)
    ]

os.makedirs("logos", exist_ok=True)
os.makedirs("informes", exist_ok=True)

# 2. Bajar escudos
for eq in equipos:
    try:
        logo_url = eq.get('logo_url') or f"https://media.api-sports.io/football/teams/{eq['id']}.png"
        res = requests.get(logo_url, timeout=10)
        if res.status_code == 200:
            open(f"logos/{eq['id']}.png", "wb").write(res.content)
            print(f"Logo {eq['EQUIPO']} ok")
    except Exception as e:
        print(f"Error logo {eq['EQUIPO']}: {e}")

# 3. Generar PDF
doc = fitz.open()
page = doc.new_page(width=842, height=595)
page.insert_text((30,30), f"INFORME SEMANAL LaLiga 26/27 - {date.today()} - Jornada auto", fontsize=14)
page.insert_text((30,50), f"Fuente: API-Football | PJ PTS G E P GF GC DG + Escudo", fontsize=9)

x0, y0 = 30, 75
col_widths = [35, 35, 150, 35, 35, 30, 30, 30, 35, 35, 35]
headers = ["POS","ESCUDO","EQUIPO","PJ","PTS","G","E","P","GF","GC","DG"]

for i,h in enumerate(headers):
    rx = x0 + sum(col_widths[:i])
    page.draw_rect(fitz.Rect(rx, y0, rx+col_widths[i], y0+22), color=(0,0,0), fill=(0.2,0.2,0.2))
    page.insert_text((rx+5, y0+15), h, fontsize=8, color=(1,1,1))

y = y0+22
for eq in equipos:
    if y > 560:
        page = doc.new_page(width=842, height=595)
        y = 30
    bg = (0.85,0.92,0.85) if eq["POS"]<=4 else (1,1,0.8) if eq["POS"]<=6 else (0.96,0.78,0.78) if eq["POS"]>=18 else (1,1,1)
    for i in range(len(headers)):
        rx = x0 + sum(col_widths[:i])
        page.draw_rect(fitz.Rect(rx, y, rx+col_widths[i], y+20), color=(0.5,0.5,0.5), fill=bg)

    page.insert_text((x0+12, y+13), str(eq["POS"]), fontsize=8)
    logo_path = f"logos/{eq['id']}.png"
    if os.path.exists(logo_path):
        try:
            page.insert_image(fitz.Rect(x0+36, y+2, x0+68, y+18), filename=logo_path)
        except:
            pass
    page.insert_text((x0+72, y+13), eq["EQUIPO"][:22], fontsize=8)
    page.insert_text((x0+225, y+13), str(eq["PJ"]), fontsize=8)
    page.insert_text((x0+260, y+13), str(eq["PTS"]), fontsize=8)
    page.insert_text((x0+295, y+13), str(eq["G"]), fontsize=8)
    page.insert_text((x0+325, y+13), str(eq["E"]), fontsize=8)
    page.insert_text((x0+355, y+13), str(eq["P"]), fontsize=8)
    page.insert_text((x0+385, y+13), str(eq["GF"]), fontsize=8)
    page.insert_text((x0+420, y+13), str(eq["GC"]), fontsize=8)
    page.insert_text((x0+455, y+13), str(eq["DG"]), fontsize=8)
    y+=20

nombre_pdf = f"informes/Informe_LaLiga_{date.today()}.pdf"
doc.save(nombre_pdf)
print(f"PDF CREADO: {nombre_pdf}")
