import os
from dotenv import load_dotenv
from icalendar import Calendar

from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
import re

# -- BDD des groupes --

try: 
    with open("resources.json", "r", encoding="utf-8") as f:
        RESOURCES_DB = json.load(f)
except FileNotFoundError:
    RESOURCES_DB = {}
    print('resources.json est introuvable')


def parse_ics(ics_data: bytes):
    cal = Calendar.from_ical(ics_data)
    events = []

    for component in cal.walk('VEVENT'):
        summary = str(component.get("SUMMARY", "Cours sans titre"))
        location = str(component.get('LOCATION', 'Salle non précisée'))
        description = str(component.get("DESCRIPTION", ""))

        start = component.get('DTSTART').dt.isoformat() if component.get("DTSTART") else None
        end = component.get('DTEND').dt.isoformat() if component.get("DTEND") else None

        events.append({
            'title': summary,
            'location': location,
            'professor': clean_description(description),
            'start_time': start,
            'end_time': end
        })
    
    return events

CATEGORY_ORDER = [
    "1A Prépa",
    "2A Prépa",
    "1A Ingé Etu",
    "1A Ingé App",
    "2A Ingé Etu",
    "2A Ingé App",
    "3A Ingé Etu",
    "3A Ingé App",
]

SHORT_NAME_PREFIX_ORDER = ["TP", "Gr", "Pr"]

def short_name_sort_key(short_name):
    match = re.match(r"([A-Za-zÀ-ÿ]+)(\d+)", short_name)
    if not match:
        return (99, short_name)  # fallback si le format ne matche pas (ex: "S2C", "SEC"...)

    prefix, number = match.group(1), int(match.group(2))

    if prefix in SHORT_NAME_PREFIX_ORDER:
        prefix_rank = SHORT_NAME_PREFIX_ORDER.index(prefix)
    else:
        prefix_rank = len(SHORT_NAME_PREFIX_ORDER)  # préfixe inconnu → après les connus

    return (prefix_rank, number)

def category_sort_key(cat_name):
    if cat_name in CATEGORY_ORDER:
        return (0, CATEGORY_ORDER.index(cat_name))
    return (1, cat_name)


def clean_description(description: str):
    lines = [line.strip() for line in description.split('\n') if line.strip()]

    prof_name = ""  
    
    if not lines:
        return prof_name

    if lines[-1].startswith("(Exporté"):
        lines.pop()

    if len(lines) > 1:
        prof_name = lines[-1]

    return prof_name

load_dotenv()
app = FastAPI(title="EsiEDT")

# -- CORS config --
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://esiedt.anttonc.fr", "http://localhost:3000", "http://localhost:5173", "http://192.168.1.34:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# -- Routes --


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    
@app.get("/api/schedule/{resource_id}")
@cache(expire=7200)
async def get_schedule(resource_id: str):
    USERNAME = os.getenv("AGALAN_USERNAME", "wrong username")
    PASSWORD = os.getenv("AGALAN_PASSWORD", "wrong password")


    ADE_URL = f"https://edt.grenoble-inp.fr/directCal/2026-2027/etudiant/esisar?resources={resource_id}"
    
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(ADE_URL, auth=(USERNAME, PASSWORD))
            
            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Identifiants refusés")
            elif response.status_code != 200:
                print(f"Erreur ADE: {response.status_code} - {response.text}")
                raise HTTPException(status_code=502, detail="ADE est encore en panne :(")
            
            ics_content = response.content

            structured_data = parse_ics(ics_content)


            return {
                "status": "success",
                "resource_id": resource_id,
                "total_events": len(structured_data),
                "events": structured_data
            }

        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="ADE est en grève :(")
        

@app.get("/api/search")
async def search_resources(q: str):
    """
        Recherche un groupe dans la base de données
    """

    if not q or len(q) < 1:
        return {"status": "error", "message": "Entrez au moins 1 caractère"}
    
    query_lower = q.lower()
    results = []

    for name, resource_id in RESOURCES_DB.items():
        if query_lower in name.lower():
            results.append({
                "name": name,
                "id": resource_id
            })

    results = sorted(results, key=lambda x: x["name"])


    return {
        "status": "success",
        "query": q,
        "total_results": len(results),
        "results": results
    }


@app.get("/api/groups")
async def get_grouped_resources():
    """
    Organise la base de données brute en catégories structurées (Onglets)
    en fusionnant automatiquement les semestres (S5+S6, S7+S8).
    """
    temp_categories = {}
    
    for full_name, resource_id in RESOURCES_DB.items():
        # 1. Traitement des classes "Ingénieur"
        if "-Ingé-" in full_name:
            parts = full_name.split('-')
            year = parts[0]
            status = parts[2]
            category = f"{year} Ingé {status}"  # une seule catégorie, peu importe le cas

            if "-Pr" in full_name:
            	# Groupes de projet : pas de semestre dans le nom, on garde tel quel
            	short_name = parts[-1]
            elif len(parts) > 3 and parts[3].startswith('S') and parts[3][1:].isdigit():
            	# 4ème partie = un semestre (ex: 'S5', 'S9') → on l'ignore
            	short_name = "-".join(parts[4:])
            else:
            	# Pas de semestre (ex: 'TP1' pour les Apprentis) → on le garde
            	short_name = "-".join(parts[3:])
                          
        elif "-Prépa" in full_name:
            parts = full_name.split('-')
            category = f"{parts[0]} Prépa"
            short_name = "-".join(parts[2:])
            
        else:
            category = "Autres"
            short_name = full_name
            
        # Initialisation de la catégorie si elle n'existe pas
        if category not in temp_categories:
            temp_categories[category] = {}
            
        # Initialisation du groupe s'il n'existe pas
        if short_name not in temp_categories[category]:
            temp_categories[category][short_name] = {
                "full_name": f"{category} - {short_name}",
                "short_name": short_name,
                "ids": [] # On utilise une liste pour stocker plusieurs IDs !
            }
            
        # On ajoute l'identifiant au groupe
        temp_categories[category][short_name]["ids"].append(resource_id)
        
    # Formatage final et tri
    final_data = {}
    for cat, groups in sorted(temp_categories.items(), key=lambda item: category_sort_key(item[0])):
        formatted_groups = []
        for short_name, data in sorted(groups.items(), key=lambda item: short_name_sort_key(item[0])):            # On transforme la liste d'IDs en une chaîne séparée par des virgules
            # ex: ["5934", "5961"] -> "5934,5961"
            data["id"] = ",".join(data["ids"])
            del data["ids"] # Nettoyage de la liste temporaire
            formatted_groups.append(data)
            
        final_data[cat] = formatted_groups
        
    return {
        "status": "success",
        "categories_count": len(final_data),
        "data": final_data
    }
