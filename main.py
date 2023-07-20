import requests
from bs4 import BeautifulSoup
import csv


def parse_dealerships(cities):
    url = "https://omvic.powerappsportals.com/registrant-search/find-dealership-salesperson/"
    response = requests.get(url)
    response.raise_for_status()


    print(response.content) #debugging

    soup = BeautifulSoup(response.content, "html.parser")

    dealerships = []
    # Find the table containing the dealership links
    dealership_table = soup.find("table", id="dealershipSearchResultsTable")

    print(dealership_table) #debug
    # Find all dealership links within the table
    dealership_links = dealership_table.find_all("a")
    print(dealership_links) #debug
    for link in dealership_links:
        dealership_name = link.get_text(strip=True)
        dealership_url = link["href"]
        dealership_city = link.find_next("td").get_text(strip=True)

        print("Name:", dealership_name) #debug
        print("URL:", dealership_url) #debug
        print("City:", dealership_city) #debug


        if dealership_city in cities:
            # Append dealership details to the list
            dealerships.append({
                "ref_id": link["href"].split("id=")[-1],
                "legal_name": dealership_name,
                "business_name": "",
                "registration_status": "",
                "web_url": f"https://omvic.powerappsportals.com/registrant-search/find-dealership-salesperson/{dealership_url}",
                "website": "",
                "emails": "",
                "phones": "",
                "country": "",
                "state": "",
                "city": dealership_city,
                "zip": "",
                "address": "",
                "dealer_sub_class": "",
                "extra_fields": ""
            })

    return dealerships


def parse_salespersons(dealership_url):
    url = "https://omvic.powerappsportals.com/registrant-search/find-dealership-salesperson/" + dealership_url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup.prettify()) #debug

    salespersons = []

    # Find all salesperson names
    salesperson_names = soup.find_all("span", class_="....")

    for name in salesperson_names:
        salesperson_name = name.get_text(strip=True)

        # Append salesperson details to the list
        salespersons.append({
            "ref_id": "",
            "first_name": salesperson_name,
            "last_name": "",
            "registration_status": "",
            "expiry_date": "",
            "reports": "",
            "dealerships": ""
        })

    return salespersons


def save_dealerships(dealerships):
    if not dealerships:
        print("No dealerships found.") #debug
        return

    fieldnames = dealerships[0].keys()

    with open('data/omvic_dealerships.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dealerships)


def save_salespersons(salespersons):
    fieldnames = salespersons[0].keys()

    with open('data/omvic_salespersons.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(salespersons)


# Define the cities to scrape
cities_to_scrape = ["Toronto", "Ottawa", "Mississauga"]

# Parse dealerships
dealerships = parse_dealerships(cities_to_scrape)

# Save dealerships as CSV
save_dealerships(dealerships)

# Parse salespersons for each dealership
for dealership_item in dealerships:
    dealership_url = dealership_item["web_url"]
    salespersons = parse_salespersons(dealership_url)
    dealership_item["dealerships"] = [salesperson["ref_id"] for salesperson in salespersons]

    # Save salespersons as CSV
    save_salespersons(salespersons)
