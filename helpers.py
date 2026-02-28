import os
import requests


def search_by_species(species):
    return requests.get(
        "https://api.floraapi.com/v1/search/",
        headers={"Authorization": f"Bearer {os.environ.get("FLORA_API_KEY")}"},
        params={
        }
    )

def get_environmental_impact(zip):
    return requests.get(
        "https://api.floraapi.com/v1/species/1233/climate-match",
        headers={"Authorization": f"Bearer {os.environ.get("FLORA_API_KEY")}"},
        params={"zip_code": zip}
    )