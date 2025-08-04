#!python
import os
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import json
import us

#         "FAA": "", "IATA": "", "ICAO": "", "Airport": "", "Role": "", "Enplanements": ""
keys = ["FAA", "IATA", "ICAO", "Airport", "Role", "Enplanements"]

openai_api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI(
    api_key=openai_api_key,
)

url = "https://en.wikipedia.org/wiki/List_of_airports_in_the_United_States"


# Fetch the webpage content
response = requests.get(url)
html_content = response.text

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the target table using its class. Note: "jquery-tablesorter" is often omitted as it's dynamically applied
table = soup.find('table', class_='wikitable sortable')

# Initialize lists to store headers and rows
headers = []
data = []

def state_header(row_dict):
    for key in keys:
        if row_dict[key] != "":
            return False
    return True

def dump_completion(completion, answer):
    print(f"{answer}: {completion}")

if table:
    # Extract headers
    header_row = table.find('tr')
    if header_row:
        headers = [th.get_text(strip=True) for th in header_row.find_all('th')]

    state = "UNKNOWN"
    state_abbreviation = "UNKNOWN"
    all_iata = set()
    # Extract data rows
    for row in table.find_all('tr')[1:]:  # Skip the header row
        row_data = [td.get_text(strip=True) for td in row.find_all('td')]
        # Create a dictionary for each row, mapping headers to data
        row_dict = dict(zip(headers, row_data))
        if state_header(row_dict):
            state = row_dict["City"]
            state_object = us.states.lookup(state)
            if state_object:
                state_abbreviation = state_object.abbr
            else:
                state_abbreviation = "UNKNOWN"
            continue

        row_dict["State"] = state
        row_dict["StateAbbreviation"] = state_abbreviation
        if row_dict["IATA"] == "":
            raise Exception(f"IATA is empty for {row_dict}")
        iata = row_dict["IATA"]
        #****************
        if iata != "PDX":
            continue
        #****************

        if iata in all_iata:
            raise Exception(f"IATA {iata} is not unique")
        city = row_dict["City"]
        all_iata.add(iata)
        #q = f"First determine the recommended public ssid to use for wifi configuration for airport {iata} in {city}. Then reduce the that answer down to a single SSID wifi string"
        q = f"the recommended public ssid to use for wifi configuration for airport {iata} in {city}"
        print(q)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": q
                }
            ],
        )
        answer = completion.choices[0].message.content
        dump_completion(completion, answer)
        row_dict["SSID"] = answer
        data.append(row_dict)

# Convert the list of dictionaries to a JSON array
AIRPORTS_JSON = "public/airports.json"
print(json.dumps(data, indent=4))
print(f"updating {AIRPORTS_JSON}")
with open(AIRPORTS_JSON, 'w') as f:
    json.dump(data, f, indent=4)  # Use indent for pretty-printing (optional)
