import os
from dotenv import load_dotenv
from icalendar import Calendar

from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
# from fastapi_cache.decorator import cache
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
import re
from datetime import datetime, timezone, timedelta
import asyncio
import logging

load_dotenv()

# -- Global variables --
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

LAST_GOOD_RESPONSE: dict[str, dict] = {}
CACHE_DURATION_SECONDS = 7200

SIMULATE_ADE_DOWN = False

FIXTURE_MODE = os.getenv("FIXTURE_MODE", "false") == "true"
FIXTURE_ICS_PATH = "ADECal.ics"



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



def short_name_sort_key(short_name):
    match = re.match(r"([A-Za-zÀ-ÿ]+)(\d+)", short_name)
    if not match:
        return (99, short_name)  # fallback si le format ne matche pas (ex: "S2C", "SEC"...)

    prefix, number = match.group(1), int(match.group(2))

    if prefix in SHORT_NAME_PREFIX_ORDER:
        prefix_rank = SHORT_NAME_PREFIX_ORDER.index(prefix)
    else:
        prefix_rank = len(SHORT_NAME_PREFIX_ORDER)

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
    asyncio.create_task(daily_refresh_loop())


@app.get("/api/schedule/{resource_id}")
# @cache(expire=10)
async def get_schedule(resource_id: str):
    USERNAME = os.getenv("AGALAN_USERNAME", "wrong username")
    PASSWORD = os.getenv("AGALAN_PASSWORD", "wrong password")

    cached = LAST_GOOD_RESPONSE.get(resource_id)
    now = datetime.now().timestamp()

    if cached and (now - cached["fetched_at"]) < CACHE_DURATION_SECONDS:
        return cached['data']

    # ICS local
    if FIXTURE_MODE:
        with open(FIXTURE_ICS_PATH, "rb") as f:
            ics_content = f.read()

        structured_data = parse_ics(ics_content)
        result = {
            "status": "success",
            "resource_id": resource_id,
            "total_events": len(structured_data),
            "fetched_at": datetime.fromtimestamp(now, tz=timezone.utc).isoformat(),
            "events": structured_data
        }
        LAST_GOOD_RESPONSE[resource_id] = {"data": result, "fetched_at": now}
        return result


    month = datetime.now().month
    year = datetime.now().year - 1 if month < 8 else datetime.now().year
    params = "resourcess" if SIMULATE_ADE_DOWN else "resources" # USEFUL FOR DEBUG AND SIMULATE ADE DOWN
    ADE_URL = f"https://edt.grenoble-inp.fr/directCal/{year}-{year+1}/etudiant/esisar?{params}={resource_id}&startDay=31&startMonth=08&startYear={year}&endDay=31&endMonth=07&endYear={year+1}"
    
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(ADE_URL, auth=(USERNAME, PASSWORD))
            
            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="401 : Identifiants refusés, envoyez un mail à contact@anttonc.fr")
            elif response.status_code != 200:
                print(f"Erreur ADE: {response.status_code} - {response.text}")
                if cached:
                    return cached["data"]
                raise HTTPException(status_code=502, detail="ADE est encore en panne :(")
            
            ics_content = response.content
            structured_data = parse_ics(ics_content)

            result = {
                "status": "success",
                "resource_id": resource_id,
                "total_events": len(structured_data),
                "fetched_at": datetime.fromtimestamp(now, tz=timezone.utc).isoformat(),
                "events": structured_data
            }

            LAST_GOOD_RESPONSE[resource_id] = {"data": result, "fetched_at": now}
            return result 

        except httpx.RequestError:
            if cached:
                return cached["data"]

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
            category = f"{year} Ingé {status}"

            if "-Pr" in full_name:
            	short_name = parts[-1]
            elif len(parts) > 3 and parts[3].startswith('S') and parts[3][1:].isdigit():
            	short_name = "-".join(parts[4:])
            else:
            	short_name = "-".join(parts[3:])
                          
        elif "-Prépa" in full_name:
            parts = full_name.split('-')
            category = f"{parts[0]} Prépa"
            short_name = "-".join(parts[2:])
            
        else:
            category = "Autres"
            short_name = full_name
            
        if category not in temp_categories:
            temp_categories[category] = {}
            
        if short_name not in temp_categories[category]:
            temp_categories[category][short_name] = {
                "full_name": f"{category} - {short_name}",
                "short_name": short_name,
                "ids": [] 
            }
            
        temp_categories[category][short_name]["ids"].append(resource_id)
        
    # Formatage final et tri
    final_data = {}
    for cat, groups in sorted(temp_categories.items(), key=lambda item: category_sort_key(item[0])):
        formatted_groups = []
        for short_name, data in sorted(groups.items(), key=lambda item: short_name_sort_key(item[0])): 
            data["id"] = ",".join(data["ids"])
            del data["ids"] 
            formatted_groups.append(data)
            
        final_data[cat] = formatted_groups
        
    return {
        "status": "success",
        "categories_count": len(final_data),
        "data": final_data
    }


# Config logging
refresh_logger = logging.getLogger("daily_refresh")
refresh_logger.setLevel(logging.INFO)

_file_handler = logging.FileHandler("daily-refresh.log", encoding="utf-8")
_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
refresh_logger.addHandler(_file_handler)

def seconds_units_next_round(hrs: int = 5, min: int = 0) -> float:
    now = datetime.now()
    next_run = now.replace(hour=hrs, minute=min, second=0, microsecond=0)

    if next_run <= now:
        next_run += timedelta(days=1)

    return (next_run - now).total_seconds()

async def refresh_all_resources():
    """
        rafraichit le cache de toutes les ressouces ics
    """
    resource_ids = set(RESOURCES_DB.values())
    # resource_ids = set(list(resource_ids)[:3])
    refresh_logger.info(f"Starting daily .ics refresh - {len(resource_ids)} to fetch")

    success_count = 0
    errors = []

    for id in resource_ids:
        try:
            await get_schedule(id)
            success_count += 1
        except Exception as e:
            errors.append(f"{id} : {e}")

        await asyncio.sleep(4)
    
    refresh_logger.info(f"Completed. Success : {success_count}/{len(resource_ids)}. Errors : {len(errors)}")

    if errors:
        for err in errors:
            refresh_logger.warning(f"Error {err}")

async def daily_refresh_loop():
    while True:
        wait_seconds = seconds_units_next_round(hrs=7, min=00)
        refresh_logger.info(f"{wait_seconds / 3600:.1f}h until next refresh")
        await asyncio.sleep(wait_seconds)
        await refresh_all_resources()




# /!\ FOR TEST AND LOCAL DEVELOPMENT ONLY /!\
# DO NOT EXPOSE THIS ROUTE ON PROD

# @app.post("/debug/toogle-ade-down")
# async def toogle_ade_down():
#     """
#     Cette route permet de simuler ADE en panne en corrompant l'url, pour tester la robustesse du système de cache
#     """
#     global SIMULATE_ADE_DOWN
#     SIMULATE_ADE_DOWN = not SIMULATE_ADE_DOWN
#     return {"simulate_ade_down": SIMULATE_ADE_DOWN}


