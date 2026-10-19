import requests

COVERED_CITIES = ["Jersey Village city"]
COVERED_ISDS = ["Cypress-Fairbanks Independent School District"]

def lookup_address(address):
    url = "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress"
    params = {
        "address": address,
        "benchmark": "Public_AR_Current",
        "vintage": "Current_Current",
        "layers": "all",
        "format": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()

    matches = data["result"]["addressMatches"]

    if not matches:
        return {"covered": False, "reason": "Address not found"}

    match = matches[0]
    lat = match["coordinates"]["y"]
    lon = match["coordinates"]["x"]
    geographies = match["geographies"]

    # get city name
    places = geographies.get("Incorporated Places", [])
    city = places[0]["NAME"] if places else None

    # get school district name
    isds = geographies.get("Unified School Districts", [])
    isd = isds[0]["NAME"] if isds else None

    print("City:", city)
    print("ISD:", isd)

    # check if we cover this address
    city_covered = city in COVERED_CITIES
    isd_covered = isd in COVERED_ISDS

    if not city_covered and not isd_covered:
        return {
            "covered": False,
            "reason": f"We don't cover {city or 'this area'} yet",
            "lat": lat,
            "lon": lon
        }

    return {
        "covered": True,
        "lat": lat,
        "lon": lon,
        "city": city,
        "isd": isd,
        "city_covered": city_covered,
        "isd_covered": isd_covered
    }

if __name__ == "__main__":
    # test with Jersey Village address
    print("--- Jersey Village (should be covered)")
    print(lookup_address("16327 Lakeview Dr Jersey Village TX"))

    # test with address outside coverage
    print("--- Houston address (should not be covered)")
    print(lookup_address("1600 Smith St Houston TX"))

    print("--- Cypress address (CFISD but no city)")
    print(lookup_address("15000 Eldridge Pkwy Cypress TX 77429"))

    print("--- Cypress address (CFISD but no city)")
    print(lookup_address("9811 Huffmeister Rd Cypress TX 77095"))