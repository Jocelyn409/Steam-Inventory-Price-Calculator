import time
import requests as req
import json


def calculate_total_price(input_dict):
    total_price = 0
    number = 0
    for url in input_dict:
        number = number + 1
        item_price = get_item_price(url) * input_dict[url]
        total_price = total_price + item_price
        total_price = round(total_price, 2)
        if number == 10:
            time.sleep(1)
    print(total_price)


def get_item_price(item):  # Add item_count as a parameter.
    currency = 1  # Hard coded currency (USD). Can be changed later if needed.
    item = item.replace("https://steamcommunity.com/market/listings/", "")
    split_item = item.split("/")  # Splits listing by game id and market hash name.
    game_id = split_item[0]
    market_hash_name = split_item[1]

    response = req.get("https://steamcommunity.com/market/priceoverview/"
                       "?appid=" + game_id +  # ID for specific game.
                       "&market_hash_name=" + market_hash_name +  # Item.
                       "&currency=" + str(currency))  # Currency.
    item_information = json.loads(response.text)  # Converts the json string to a dictionary.
    print(item_information)  # Debugger print.

    # if (item_information is None) or \
    #         (item_information["success"] not in item_information) or \
    #         (item_information["success"] is not True):
    #     raise Exception("Error getting item price information.")

    # Gets the lowest price (not including currency symbol).
    return float(item_information["lowest_price"][1:].replace(",", ""))


def insert_item():
    with open("item_list.json", "r") as read_json_file:
        item_dictionary = json.load(read_json_file)

    answer = "Y"
    while answer == "Y":
        url = input("Enter a URL for an item: ")
        # If there is a matching URL, don't add to file. Have it as a function.
        count = int(input("Enter the number of items: "))
        item_dictionary.update({url: count})
        answer = input("Continue? Y/N: ").upper()

    json_object = json.dumps(item_dictionary, indent=4)

    with open("item_list.json", "w") as write_json_file:
        write_json_file.write(json_object)


if __name__ == "__main__":
    with open("item_list.json", "r") as calculate_json:
        calculate_dictionary = json.load(calculate_json)

    calculate_total_price(calculate_dictionary)

    # for url in calculate_dictionary:
    #     price = get_item_price(url)
    #     print(price * calculate_dictionary[url])

    # see full list of items and their individual prices with total price for that individual item.

    # need to update count somehow. if new count is 0, simply remove the item from the list...?

    #insert_item()
