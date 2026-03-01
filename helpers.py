import os
import requests
import pandas as pd


def search_by_species(scientific_name):
    API_KEY_TREFLE = "usr-PhmgQUg-6n6VNe9PDJPs7pA9rYKI2-0GmN2UPHY70ZE"  # or just paste your key as a string
    url_tre = "https://trefle.io/api/v1/plants"

    headers_tre = {
        "Authorization": f"Bearer {API_KEY_TREFLE}"
    }

    params_tre = {
        "token": API_KEY_TREFLE,
        "filter[scientific_name]": scientific_name
    }

    response_tre = requests.get(url_tre, headers=headers_tre, params=params_tre)
    data = response_tre.json().get("data", [])
    if data:
        return data[0]
    return None



def get_environmental_impact(zip):
    return requests.get(
        "https://api.floraapi.com/v1/species/1233/climate-match",
        headers={"Authorization": f"Bearer {os.environ.get('FLORA_API_KEY')}"},
        params={"zip_code": zip}
    )

def get_reccommended_plants(state, hardiness):

    response = requests.get(
        "https://api.floraapi.com/v1/search/",
        headers={"Authorization": "Bearer pk_m0ckvLeKWK5suFEMN8KEQFUrtBqOhdHO"},
        params={
            "state": state,
            # "flower_color":"white", # we could add this back in to narrow results
            "native_only": True,  # hard coded
            "plant_habit": "Forb",  # hard coded
            "limit": 500,
            "hardiness_zone_min": hardiness,
            "hardiness_zone_max": hardiness
        }
    )

    data = response.json()
    # dictionary with 5 keys:  results is main data
    # ['results', 'total_count', 'page_size', 'offset', 'has_more']

    species_list = data["results"]
    species_names = []

    for item in species_list:
        name = item["scientific_name"]
        if not name.__contains__("×"):
            if name.count(" ") > 1:
                name = " ".join(name.split(" ")[0:2])
            species_names.append(name)

    # print(species_names)
    # print(len(species_names))

    # scientific_names = ["Solidago canadensis", "Monarda fistulosa"]
    # joined_names = ",".join(scientific_names)
    joined_names = ",".join(species_names)

    # scientific_name = "Solidago canadensis"

    API_KEY_TREFLE = "usr-FxdeRGHbUg1G1ehQa4gQfTzbvhJdaYlHjiUoENpegLw"  # or just paste your key as a string
    url_tre = "https://trefle.io/api/v1/plants"

    params_tre = {
        "token": API_KEY_TREFLE,
        "filter[scientific_name]": joined_names,
        "filter[fields]": "id",
        "page": 1,
        "per_page": 1000
    }

    all_plants = []
    pindex = 1
    url_garbage = True
    while url_garbage:
        resp = requests.get(url_tre,
                                {
                                    "token": API_KEY_TREFLE,
                                    "filter[scientific_name]": joined_names,
                                    "filter[fields]": "id",
                                    "page": pindex,
                                    "per_page": 20
                                }
                                )
        print(f"DEBUG - Status: {resp.status_code}, Body: {resp.text[:500]}")
        response = resp.json()
        all_plants.extend(response["data"])
        url_garbage = response["links"].keys().__contains__("next")
        # url_garbage = response["links"]["next"]
        pindex += 1

    # response_tre = requests.get(url_tre, headers=headers_tre, params=params_tre)
    # response_tre = requests.get(url_tre, params=params_tre)
    # print(response_tre.text)

    # data = response_tre.json()
    data = all_plants  # .json()
    print(type(data[0]))
    plant_id_list = []
    '''
    links="links"
    print("hello\n")
    print(data[links])
    print(type(data[links]))
    print(len(data[links]))
    '''
    for plant in data:  # ["data"]:
        # print({"id": plant["id"]})
        plant_id_list.append(plant["id"])

    # plant_id = plant["id"]

    # everything above this line works-------------------------------------------------
    # everything below also works but should be threaded___________________________

    '''
    print(len(plant_id_list))
    for i in plant_id_list:
        url_species = f"https://trefle.io/api/v1/species/{i}"

        response_species = requests.get(url_species, params={"token": API_KEY_TREFLE})
        species_data = response_species.json()

        plant_info = species_data.get("data", {})

        growth = plant_info.get("growth") or {}

        print({
            #"scientific_name": plant_info.get("scientific_name"),
            #"common_name": plant_info.get("common_name"),
            "light": growth.get("light"),
            "soil_ph_min": growth.get("ph_minimum"),
            "soil_ph_max": growth.get("ph_maximum"),
            "minimum_temperature": growth.get("minimum_temperature"),
            "maximum_temperature": growth.get("maximum_temperature"),
            "minimum_precipitation": growth.get("minimum_precipitation"),
            "maximum_precipitation": growth.get("maximum_precipitation"),
            "atmospheric_humidity": growth.get("atmospheric_humidity"),
        })
    '''

    from concurrent.futures import ThreadPoolExecutor, as_completed
    import itertools

    # List your API keys
    API_KEYS = [
        "usr-YhYS8ARjDprTx_-a6bfWg3V6ZdBlRftXqd2TiyTQanE",
        "usr-3A4t0TZ5yt6MnXBLGMtCOjoQ41mJWXqhtvbIzMOO-p4",
        "usr-FxdeRGHbUg1G1ehQa4gQfTzbvhJdaYlHjiUoENpegLw",
        "usr-LXMRKJ09yf9A7A5NxkEbLz_rWVaz2EQW3Ygd1rzrG9o",
        "usr-U3dDTWSJX92UUVyDXklHpKTXkqft5DDB01qLmatdLgY",
        "usr-AnNjwl8kHZkUdbbJGEn3a02BZBVEJq6fTS5c39rlWCk",
        "usr-x6xOz3oAtGZ8muxXiSVrZhTsfYIIXgSI9KkVV8DCoWU"
    ]

    # Create a cycling iterator over keys
    key_cycle = itertools.cycle(API_KEYS)

    # plant_id_list =   # your plant IDs

    def fetch_growth_with_key_rotation(plant_id):
        """Fetch growth data using rotating API keys to avoid hitting rate limits."""
        url_species = f"https://trefle.io/api/v1/species/{plant_id}"
        api_key = next(key_cycle)  # grab the next API key
        try:
            response_species = requests.get(url_species, params={"token": api_key}, timeout=10)
            response_species.raise_for_status()
            species_data = response_species.json()
            plant_info = species_data.get("data", {})
            growth = plant_info.get("growth") or {}
            return {
                "common_name": plant_info.get("common_name"),
                "scientific_name": plant_info.get("scientific_name"),
                "image_url": plant_info.get("image_url"),
                "light": growth.get("light"),
                "soil_ph_min": growth.get("ph_minimum"),
                "soil_ph_max": growth.get("ph_maximum"),
                # "minimum_temperature": growth.get("minimum_temperature"),
                # "maximum_temperature": growth.get("maximum_temperature"),
                # "minimum_precipitation": growth.get("minimum_precipitation"),
                # "maximum_precipitation": growth.get("maximum_precipitation"),
                # "atmospheric_humidity": growth.get("atmospheric_humidity")

            }
        except Exception as e:
            print(f"Error fetching {plant_id} with key {api_key}: {e}")
            return None

    '''"light": growth.get("light"),
               "soil_ph_min": growth.get("ph_minimum"),
               "soil_ph_max": growth.get("ph_maximum"),
               "minimum_temperature": growth.get("minimum_temperature"),
               "maximum_temperature": growth.get("maximum_temperature"),
               "minimum_precipitation": growth.get("minimum_precipitation"),
               "maximum_precipitation": growth.get("maximum_precipitation"),
               "atmospheric_humidity": growth.get("atmospheric_humidity"),
    '''

    results = []

    # Use threads for concurrency
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_growth_with_key_rotation, pid) for pid in plant_id_list]
        for future in as_completed(futures):
            data = future.result()
            if data:
                results.append(data)

    print(f"Fetched growth data for {len(results)} plants using {len(API_KEYS)} API keys")

    # Filter out results with None pH values before creating DataFrame
    def is_valid_number(val):
        if val is None or val == "None":
            return False
        try:
            float(val)
            return True
        except (ValueError, TypeError):
            return False

    results = [r for r in results
               if is_valid_number(r.get("soil_ph_min"))
               and is_valid_number(r.get("soil_ph_max"))]

    if not results:
        return pd.DataFrame(columns=["common_name", "scientific_name", "image_url", "light", "soil_ph_min", "soil_ph_max"])

    df = pd.DataFrame(results)
    # print(df[df["species_name"].str.contains("Solidago", na=False)])

    # Convert None to NaN so dropna catches them
    df["soil_ph_min"] = pd.to_numeric(df["soil_ph_min"], errors="coerce")
    df["soil_ph_max"] = pd.to_numeric(df["soil_ph_max"], errors="coerce")
    df = df.dropna(subset=["soil_ph_min", "soil_ph_max"])

    # print(df[df["species_name"].str.contains("Solidago", na=False)])

    def plants_with_same_ph_range(df, input_species):
        # Find the input plant row
        row = df[df["scientific_name"] == input_species]

        if row.empty:
            print("Plant not found.")
            return []

        input_min = row.iloc[0]["soil_ph_min"]
        input_max = row.iloc[0]["soil_ph_max"]

        # Find overlapping ranges
        matches = df[
            df["soil_ph_min"].notna() &
            df["soil_ph_max"].notna() &
            (df["soil_ph_min"] <= input_max) &
            (df["soil_ph_max"] >= input_min)
        ]

        return matches["scientific_name"].tolist()

    similar = plants_with_same_ph_range(df, "Liatris pycnostachya")
    print(similar)

    return df