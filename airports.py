#!python
import requests
from bs4 import BeautifulSoup
import json
import us

#         "FAA": "", "IATA": "", "ICAO": "", "Airport": "", "Role": "", "Enplanements": ""
keys = ["FAA", "IATA", "ICAO", "Airport", "Role", "Enplanements"]

def state_header(row_dict):
    for key in keys:
        if row_dict[key] != "":
            return False
    return True

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
        if iata in all_iata:
            raise Exception(f"IATA {iata} is not unique")
        all_iata.add(iata)
        data.append(row_dict)

# Convert the list of dictionaries to a JSON array
json_output = json.dumps(data, indent=4)

# Print the JSON output
print(json_output)

