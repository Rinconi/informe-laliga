import requests
import fitz
from datetime import date

# Clasificacion actual - luego lo haremos automatico con API
# Por ahora usa los datos de hoy
equipos = [
    {"POS":1,"EQUIPO":"FC Barcelona","PJ":5,"PTS":15,"G":5,"E":0,"P":0,"GF":21,"GC":4,"DG":17,"id":529},
    {"POS":2,"EQUIPO":"Real Madrid","PJ":5,"PTS":12,"G":4,"E":0,"P":1,"GF":14,"GC":4,"DG":10,"id":541},
    {"POS":3,"EQUIPO":"Alaves","PJ":5,"PTS":10,"G":3,"E":1,"P":1,"GF":11,"GC":5,"DG":6,"id":542},
    {"POS":4,"EQUIPO":"Atletico Madrid","PJ":5,"PTS":10,"G":3,"E":1,"P":1,"GF":10,"GC":6,"DG":4,"id":530},
    {"POS":5,"EQUIPO":"Sevilla","PJ":5,"PTS":10,"G":3,"E":1,"P":1,"GF":8,"GC":6,"DG":2,"id":536},
    {"POS":6,"EQUIPO":"Deportivo","PJ":5,"PTS":9,"G":2,"E":3,"P":0,"GF":9,"GC":6,"DG":3,"id":556},
    {"POS":7,"EQUIPO":"Betis","PJ":4,"PTS":9,"G":3,"E":0,"P":1,"GF":5,"GC":5,"DG":0,"id":543},
    {"POS":8,"EQUIPO":"Espanyol","PJ":5,"PTS":7,"G":2,"E":1,"P":2,"GF":8,"GC":5,"DG":3,"id":540},
    {"POS":9,"EQUIPO":"Athletic Club","PJ":5,"PTS":7,"G":2,"E":1,"P":2,"GF":7,"GC":6,"DG":1,"id":531},
    {"POS":10,"EQUIPO":"Racing Santander","PJ":5,"PTS":7,"G":2,"E":1,"P":2,"GF":9,"GC":9,"DG":0,"id":2149},
    {"POS":11,"EQUIPO":"Osasuna","PJ":5,"PTS":7,"G":2,"E":1,"P":2,"GF":5,"GC":8,"DG":-3,"id":534},
    {"POS":12,"EQUIPO":"Real Sociedad","PJ":6,"PTS":7,"G":2,"E":1,"P":3,"GF":6,"GC":11,"DG":-5,"id":548},
    {"POS":13,"EQUIPO":"Levante","PJ":5,"PTS":5,"G":1,"E":2,"P":2,"GF":7,"GC":9,"DG":-2,"id":539},
    {"POS":14,"EQUIPO":"Getafe","PJ":5,"PTS":5,"G":1,"E":2,"P":2,"GF":3,"GC":6,"DG":-3,"id":546},
    {"POS":15,"EQUIPO":"Celta","PJ":6,"PTS":4,"G":0,"E":4,"P":2,"GF":3,"GC":6,"DG":-3,"id":538},
    {"POS":16,"EQUIPO":"Rayo Vallecano","PJ":5,"PTS":4,"G":1,"E":1,"P":3,"GF":8,"GC":14,"DG":-6,"id":728},
    {"POS":17,"EQUIPO":"Malaga","PJ":5,"PTS":3,"G":0,"E":3,"P":2,"GF":2,"GC":8,"DG":-6,"id":571},
    {"POS":18,"EQUIPO":"Villarreal","PJ":4,"PTS":2,"G":0,"E":2,"P":2,"GF":6,"GC":8,"DG":-2,"id":533},
    {"POS":19,"EQUIPO":"Elche","PJ":5,"PTS":2,"G":0,"E":2,"P":3,"GF":6,"GC":13,"DG":-7,"id":797},
    {"POS":20,"EQUIPO":"Valencia","PJ":5,"PTS":1,"G":0,"E":1,"P":4,"GF":1,"GC":10,"DG":-9,"id":532},
]

# Crear carpeta para logos y para informes
import os
os.makedirs("logos", exist_ok=True)
os.makedirs("informes", exist_ok=True)

# 1. Bajar escudos desde GitHub / API-Sports
print("Bajando escudos...")
for eq in equipos:
    try:
        url = f"https://media.api-sports.io/football/teams/{eq['id']}.png"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            open(f"logos/{eq['id']}.png", "wb").write(r.content)
    except:
        pass

# 2. Crear PDF
doc = fitz.open()
page = doc.new_page(width=842, height=595)
page.insert_text((30,30), f"INFORME SEMANAL LaLiga 26/27 - {date.today()}", fontsize=14)
page.insert_text((30,50), "Clasificacion: Equipo, PJ, PTS, G, E, P, GF, GC, DG + Escudo", fontsize=10)

x0, y0 = 30, 75
col_widths = [35, 35, 150, 35, 35, 30, 30, 30, 35, 35, 35]
headers = ["POS","EQUIPO","PJ","PTS","G","E","P","GF","GC","DG"]

for i,h in enumerate(headers):
    rx = x0 + sum(col_widths[:i])
    page.draw_rect(fitz.Rect(rx, y0, rx+col_widths[i], y0+22), color=(0,0,0), fill=(0.2,0.2,0.2))
    page.insert_text((rx+5, y0+15), h, fontsize=8, color=(1,1,1))

y = y0+22
for eq in equipos:
    bg = (0.85,0.92,0.85) if eq["POS"]<=4 else (1,1,0.8) if eq["POS"]<=6 else (0.96,0.78,0.78) if eq["POS"]>=18 else (1,1,1)
    for i in range(len(headers)):
        rx = x0 + sum(col_widths[:i])
        page.draw_rect(fitz.Rect(rx, y, rx+col_widths[i], y+20), color=(0.5,0.5,0.5), fill=bg)

    page.insert_text((x0+12, y+13), str(eq["POS"]), fontsize=8)
    # Logo real
    logo_path = f"logos/{eq['id']}.png"
    if os.path.exists(logo_path):
        try:
            page.insert_image(fitz.Rect(x0+36, y+2, x0+68, y+18), filename=logo_path)
        except:
            pass
    page.insert_text((x0+72, y+13), eq["EQUIPO"], fontsize=8)
    page.insert_text((x0+225, y+13), str(eq["PJ"]), fontsize=8)
    page.insert_text((x0+260, y+13), str(eq["PTS"]), fontsize=8)
    page.insert_text((x0+295, y+13), str(eq["G"]), fontsize=8)
    page.insert_text((x0+325, y+13), str(eq["E"]), fontsize=8)
    page.insert_text((x0+355, y+13), str(eq["P"]), fontsize=8)
    page.insert_text((x0+385, y+13), str(eq["GF"]), fontsize=8)
    page.insert_text((x0+420, y+13), str(eq["GC"]), fontsize=8)
    page.insert_text((x0+455, y+13), str(eq["DG"]), fontsize=8)
    y+=20
    if y > 550: # nueva pagina si hace falta
        page = doc.new_page(width=842, height=595)
        y = 30

nombre_pdf = f"informes/Informe_LaLiga_{date.today()}.pdf"
doc.save(nombre_pdf)
print(f"PDF creado: {nombre_pdf}")
