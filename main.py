def _process_link(self, link):
    dealership_name = link.get_text(strip=True)
    dealership_url = link["href"]
    dealership_city = link.find_next("td").get_text(strip=True)

    if dealership_city in self.cities_to_scrape:
        ref_id = link["href"].split("id=")[-1]
        if ref_id in self.dealerships:
            raise ValueError(f"Duplicated dealership ID: {ref_id}")
        self.dealerships[ref_id] = {
            "ref_id": ref_id,
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
        }
