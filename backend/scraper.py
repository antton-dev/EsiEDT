import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()
USERNAME = os.getenv("AGALAN_USERNAME")
PASSWORD = os.getenv("AGALAN_PASSWORD")

TREE_URL = "https://edt.grenoble-inp.fr/2026-2027/esisar/etudiant/jsp/standard/gui/tree.jsp?forceLoad=false&isDirect=true"

def parse_local_tree(file):    
    try:
        with open(file, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file} est introuvable.")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    resources_dict = {}

    links = soup.find_all('a', href=re.compile(r"javascript:check\("))
    
    for link in links:
        name = link.text.strip()
        match = re.search(r"check\((\d+)", link.get('href'))
        
        if match and name:
            resources_dict[name] = match.group(1)

    with open("resources.json", "w", encoding="utf-8") as f:
        json.dump(resources_dict, f, ensure_ascii=False, indent=4)
        
    print("OK. Données sauvegardées dans resources.json")


if __name__ == "__main__":
    parse_local_tree("tree.html")

