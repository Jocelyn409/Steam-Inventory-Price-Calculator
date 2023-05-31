import time
import requests
import json


def get_item_name(url):
    item = url.replace("https://steamcommunity.com/market/listings/", "")
    item_name = item.split("/")
    return ' '.join(item_name[1].split("%20"))


def get_item_price(item):  # Add item_count as a parameter.
    currency = 1  # Hard coded currency (1 = USD). Can be changed later if needed.
    item = item.replace("https://steamcommunity.com/market/listings/", "")
    split_item = item.split("/")  # Splits listing by game id and market hash name.
    game_id = split_item[0]  # Game ID of market listing.
    market_hash_name = split_item[1]  # Hash name of item listing.
    new_url = "https://steamcommunity.com/market/priceoverview/" \
              "?appid=" + game_id + \
              "&market_hash_name=" + market_hash_name + \
              "&currency=" + str(currency)

    while True:
        response = requests.get(new_url)
        if response.status_code == 429:
            print("Sleeping for 60 seconds to let Steam servers rest...")
            time.sleep(60)
        else:
            print(get_item_name(item) + " done...")
            break

    item_information = json.loads(response.text)  # Converts the json string to a dictionary.

    # Gets the lowest price excluding currency symbol.
    return float(item_information["lowest_price"][1:].replace(",", ""))


def calculate_total_price(input_dict):
    total_price = 0
    for url in input_dict:
        item_price = get_item_price(url) * input_dict[url]
        total_price = round(total_price + item_price, 2)
    print(total_price)


def insert_item():
    with open("item_list.json", "r") as read_json_file:
        item_dictionary = json.load(read_json_file)

    answer = "Y"
    while answer == "Y":
        url = input("Enter a URL for an item: ")
        if url in item_dictionary:
            print("Item already in JSON file.")
        elif url.startswith("https://steamcommunity.com/market/listings/"):
            try:
                count = int(input("Enter the number of items: "))
            except ValueError:
                print("An integer value must be entered.")
            else:
                if count > 0:
                    item_dictionary.update({url: count})
                    answer = input("Continue? Y/N: ").upper()
                else:
                    print("Integer value is not greater than 0, thus no item was entered.")
        else:
            print("URL entered is not valid.")

    json_object = json.dumps(item_dictionary, indent=4)
    with open("item_list.json", "w") as write_json_file:
        write_json_file.write(json_object)


def update_item():
    with open("item_list.json", "r") as read_json_file:
        update_dict = json.load(read_json_file)

    counter = 0
    print("Choose an item to update item count of: ")
    for url, amount in update_dict.items():
        counter += 1
        print("{}) {}: {}".format(counter, get_item_name(url), amount))

    try:
        number_answer = int(input("Enter number of item: "))
    except ValueError:
        print("An integer value must be entered.")
        return
    try:
        count_answer = int(input("Enter new item count: "))
    except ValueError:
        print("An integer value must be entered.")
        return

    if count_answer == 0:
        del update_dict[list(update_dict.keys())[number_answer]]
    elif isinstance(count_answer, int):
        update_dict.update({list(update_dict.keys())[number_answer]: count_answer})
    else:
        print("An integer value must be entered for both the item number and the new item count.")

    json_object = json.dumps(update_dict, indent=4)
    with open("item_list.json", "w") as write_json_file:
        write_json_file.write(json_object)


if __name__ == "__main__":
    with open("item_list.json", "r") as calculate_json:
        calculate_dictionary = json.load(calculate_json)

    # see full list of items and their individual prices with total price for that individual item.

    selection = ""
    while selection != 'Q':
        selection = input("[C] Calculate total inventory price\n"
                          "[I] Insert item\n"
                          "[U] Update item count\n"
                          "[Q] Quit program\n"
                          "Selection: ").upper()
        if selection == 'C':
            calculate_total_price(calculate_dictionary)
        elif selection == 'I':
            insert_item()
        elif selection == 'U':
            update_item()
        elif selection == 'Q':
            quit(0)
        else:
            print("Enter a valid answer.")
