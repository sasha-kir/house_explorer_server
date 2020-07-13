import requests
from bs4 import BeautifulSoup
from transliterate import translit

BASE_URL = "http://dom.mingkh.ru"


def scrape_house_info(city, street_type, street, house_type, house, block_type, block):
    address_parts = [street_type]

    # if street name consists of multiple words
    if " " in street:
        address_parts += [el.strip(".") for el in street.split()]
    else:
        address_parts += [street]

    address_parts += [house_type, house]

    if block:
        if block_type == "литер":
            block_type = "лит"
        address_parts += [block_type]
        if "стр" in block:
            address_parts += block.split()
        else:
            address_parts += [block]

    address_parts = [part.lower() for part in address_parts]
    full_address = [city, *address_parts]

    payload = {"address": "+".join(full_address), "searchtype": "house"}

    response = requests.get(BASE_URL + "/search", params=payload)

    if response.status_code != 200:
        return {"error": "Error accessing house info"}

    soup = BeautifulSoup(response.text, "html.parser")

    alert = soup.find("div", class_="alert-warning")
    if alert:
        return {"error": "No entry found for address"}

    # fetch houses from first page
    houses_table = soup.find("div", class_="table-responsive").contents[1]
    table_head, table_body = [child for child in houses_table.children if child != "\n"]
    houses = [child for child in table_body.children if child != "\n"]

    # check out results from other pages
    page_count = (
        len([el for el in soup.find("ul", class_="pagination").contents if el != "\n"])
        - 1
    )
    if page_count > 1:
        for page in range(2, page_count + 1):
            page_payload = payload.copy()
            page_payload["page"] = page
            page_response = requests.get(BASE_URL + "/search", params=page_payload)
            if page_response.status_code != 200:
                return {"error": "Error accessing house info"}

            page_soup = BeautifulSoup(page_response.text, "html.parser")
            page_houses_table = page_soup.find(
                "div", class_="table-responsive"
            ).contents[1]
            page_table_head, page_table_body = [
                child for child in page_houses_table.children if child != "\n"
            ]
            page_houses = [child for child in page_table_body.children if child != "\n"]
            houses.extend(page_houses)

    house_link = ""
    # find href and address
    for house in houses:
        link_node = house.find("a")
        link = link_node.get("href")
        address_at_link = link_node.get_text()
        current_parts = [el.strip(",.").lower() for el in address_at_link.split()]
        city_in_translit = translit(city.lower(), "ru", reversed=True)
        if set(address_parts) == set(current_parts) and city_in_translit in link:
            house_link = link
            break

    if not house_link:
        return {"error": "No entry found for address"}

    house_page = requests.get(BASE_URL + house_link)
    soup = BeautifulSoup(house_page.text, "html.parser")
    house_info_list = soup.find("dl", class_="dl-horizontal house")
    children = [child for child in house_info_list.children if child != "\n"]
    # parse house info table into dict
    info_dict = {}
    index = 0
    while index < len(children) - 1:
        key = children[index].get_text()
        value = children[index + 1].get_text()
        info_dict[key] = value
        index += 2

    return {
        "year_built": info_dict.get("Год постройки", "-"),
        "house_type": info_dict.get("Серия, тип постройки", "-"),
        "floor_count": info_dict.get("Количество этажей", "-"),
        "walls_material": info_dict.get("Материал несущих стен", "-"),
    }
