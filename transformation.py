import requests
import csv

# print("To use this API, you need a Github access token. You can generate your token here: https://superheroapi.com/index.html") # "29fad3779249c79c0301f91124be1ba7"
GITHUB_TOKEN = "29fad3779249c79c0301f91124be1ba7"  # input("Enter your Github token: ")

# todo - some simple test cases
# todo - documentation: instructions for running, brief architectural overview, any assumptions/simplifications made

def get_character_info(character_id: str, info_categories: list=None):
    print("retrieving character information")
    if not info_categories:
        return requests.get(f"https://superheroapi.com/api/{GITHUB_TOKEN}/{character_id}").json()
    else:
        res = {}
        for category in info_categories:
            r = requests.get(f"https://superheroapi.com/api/{GITHUB_TOKEN}/{character_id}/{category}").json()
            res.update(r)
        return res

def search_character(name: str):
    print("searching characters...")
    return requests.get(f"https://superheroapi.com/api/{GITHUB_TOKEN}/search/{name}").json()

def get_set_of_characters(id_list: list, info_categories: list=None):
    res = {}
    for id in id_list:
        r = get_character_info(id, info_categories)
        res[id] = r
    return res

def get_character_id(name: str):
    ids = []
    search = search_character(name)
    if not "results" in search.keys():
        print("No characters found with that name")
        return
    for char in search_character(name)["results"]:
        if name.strip().lower() in char["name"].strip().lower():
            ids.append([char["id"], char["name"], char["biography"]["full-name"]])
    if len(ids) == 1:
        print(f"ID: {ids[0][0]}, name: {ids[0][1]}")
        return ids[0][0]
    elif len(ids) > 1:
        print("Multiple characters found. Here's some info on them to help you narrow down: ")
        for id in ids:
            print(f"ID: {id[0]}, name: {id[1]}, real/other name: {id[2]}")
        return True

def parse_column_headers(data: dict):
    for key, value in data.items():
        if key == "response":
            continue
        if not key.isdigit():  # don't need if key is the character id
            yield key
        if isinstance(value, dict):
            yield from parse_column_headers(value)

def parse_data(data: dict):  # flatten results dict if multiple results
    if not isinstance(data, dict):
        return data
    items = []
    for k, v in data.items():
        if k == "response":
            continue
        if isinstance(v, dict):
            items.extend(parse_data(v).items())
        else:
            items.append((k, v))
    return dict(items)
    
def load_csv(data: dict, file_mode: str, file: str="hero_data.csv", multi_search="n"):
    fields = set(parse_column_headers(data))
    parents = ["powerstats", "appearance", "biography", "work", "connections", "image"]  # these are parent categories. Actual data headers are beneath them
    fields = [field for field in fields if field not in parents]
    fields.sort()
    print(f"writing to csv file: {file}")
    with open(file, file_mode) as csvfile:
        writer = csv.DictWriter(csvfile, fields)
        writer.writeheader()
        if multi_search == "y":
            parsed_data = {k: parse_data(v) for k, v in data.items()}
            for item in parsed_data.values():
                writer.writerow(item)
        else:
            parsed_data = parse_data(data)
            writer.writerow(parsed_data)
    print("done")

def validate_input(user_input: str, reset: int=0, y_n: bool=False):
    if reset:
        print(end=f"> Invalid input\r", flush=True)
        print(f"\b", end=f"\r{user_input}: ", flush=True)
    else:
        print(f"{user_input}: \b", end=f"\r{user_input}: ", flush=True)

    inp = input()
    if len(inp)==0:
        inp = validate_input(user_input, reset=1)
    elif y_n:
        if inp not in ["y", "n"]:
            inp = validate_input(user_input, reset=1, y_n=True)
    return inp

def user_input_process():
    data = {}
    req = None
    print("Welcome to the Superhero API! Get information on most heroes/villains you can think of, and dump it into a spreadsheet")
    print("If you would like data on multiple characters, you will need their character ids first. You can find a list of characters and their ids here: https://superheroapi.com/ids.html.")
    multi_search = validate_input("Do you want information on multiple characters? [y/n]", y_n=True)
    if multi_search == "y":
        ids = validate_input("Please provide the ids for the characters you want, separated by spaces")
        data = get_set_of_characters(ids.split())  # gets all categories of data by default. Could expand to specify categories in future
    if multi_search == "n":
        while not req:
            name = validate_input('Enter the name of the character you want info on. Include any symbols, for example "spider-man"')
            req = get_character_id(name)
        char_id = req if isinstance(req, str) else validate_input("Enter the character id: ")
        print(
            """The existing information categories are: 
            
            biography - basic biographical details
            powerstats - details on the characters powers
            appearance - general appearance of the character
            work - their occupation or day job
            connections - other characters associated they are associated with
            image - a link to an image of the character

            if you want to include all categories, just type "all"
            """
        )
        categories = validate_input("Enter the info categories you want, separated by spaces: ")
        if categories == "all":
            data = get_character_info(char_id)
        else:
            categories = categories.split()
            data = get_character_info(char_id, info_categories=categories)
    print('A spreadsheet with the name "hero_data.csv will be written to by default')
    new_file = validate_input("Do you want to create a spreadsheet by a different name? [y/n]", y_n=True)
    if new_file == "y":
        file_name = validate_input("Give the spreadsheet a name")
        load_csv(data, file_mode="w", file=f"{file_name}.csv", multi_search=multi_search)
    if new_file == "n":
        load_csv(data, file_mode="w", multi_search=multi_search)

def main():
    user_input_process()


if __name__ == "__main__":
    main()