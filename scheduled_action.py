import requests
import csv
from transformation import load_csv, get_set_of_characters

# This is an example script that could be used as a cron job/scheduled task
# to update the csv file with the latest data.
# It seems like a pretty static database though, so I don't imagine it changing frequently.

FILE_NAME = "hero_data.csv"

def update_spreadsheet():
    ids = []
    with open(FILE_NAME, "r") as csvfile:
        r = csv.reader(csvfile)
        print(f"Updating spreadsheet {FILE_NAME}")
        for line in r:
            print(f"----line--------{line}")
            ids.append(line.get("id"))
    print(f"-------ids------------{ids}")
    new_data = get_set_of_characters(ids)
    load_csv(new_data, file_mode="w", file=FILE_NAME, multi_search="y")

def main():
    update_spreadsheet()

if __name__ == "__main__":
    main()
    
