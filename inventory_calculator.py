import time
import requests
import json


def get_item_price(item):  # Add item_count as a parameter.
    currency = 1  # Hard coded currency (USD). Can be changed later if needed.
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
            print("Sleeping for 5 seconds...")
            time.sleep(5)
        else:
            break

    item_information = json.loads(response.text)  # Converts the json string to a dictionary.

    # Gets the lowest price excluding currency symbol.
    return float(item_information["lowest_price"][1:].replace(",", ""))


def calculate_total_price(input_dict):
    total_price = 0
    for url in input_dict:
        item_price = round(get_item_price(url) * input_dict[url], 2)
        total_price = total_price + item_price
    print(total_price)


def find_item(item_dict, item):
    if item in item_dict:
        return True


def insert_item():
    with open("item_list.json", "r") as read_json_file:
        item_dictionary = json.load(read_json_file)

    answer = "Y"
    while answer == "Y":
        url = input("Enter a URL for an item: ")
        if find_item(item_dictionary, url) is True:
            print("Item already in JSON file.")
        else:
            count = int(input("Enter the number of items: "))
            item_dictionary.update({url: count})
            answer = input("Continue? Y/N: ").upper()

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
        item = url.replace("https://steamcommunity.com/market/listings/", "")
        item_name = item.split("/")
        item_name = item_name[1].split("%20")
        print("{}) {}: {}".format(counter, ' '.join(item_name), amount))

    number_answer = int(input("Enter number of item: ")) - 1  # Zero based answer.
    count_answer = int(input("Enter new item count: "))

    if count_answer is 0:
        del update_dict[list(update_dict.keys())[number_answer]]
    else:
        update_dict.update({list(update_dict.keys())[number_answer]: count_answer})

    json_object = json.dumps(update_dict, indent=4)
    with open("item_list.json", "w") as write_json_file:
        write_json_file.write(json_object)


if __name__ == "__main__":
    with open("item_list.json", "r") as calculate_json:
        calculate_dictionary = json.load(calculate_json)

    # see full list of items and their individual prices with total price for that individual item.

    # need to update count somehow. if new count is 0, simply remove the item from the list...?

    selection = input("[C] Calculate total inventory price\n"
                      "[I] Insert item\n"
                      "[U] Update item count\n"
                      "Answer: ").upper()

    if selection == 'C':
        calculate_total_price(calculate_dictionary)
    elif selection == 'I':
        insert_item()
    elif selection == 'U':
        update_item()
