# Wrangle a JSON database to suit website needs
import json

print('setting up files...')
# Open the JSON file
file_name = "kanji-jouyou.json"
json_file = open(file_name, 'r')

# Set up output file
out_file = open("kanji_3.json", 'w')

# Load the file into a JSON object
print('setting up json...')
kanji_json = json.load(json_file)
kanji_list = [kanji for kanji, _ in kanji_json.items()]

# setup categories
categories = ["freq", "jlpt_new", "wk_level"]
filler = ["jlpt_old", "jlpt_new", "meanings", "readings_on", "readings_kun",
          "wk_level", "wk_meanings", "wk_readings_on", "wk_readings_kun", "wk_radicals"]

# set new values if null
book = dict()
book["freq"] = 2500
book["jlpt_new"] = 0
book["wk_level"] = 70

# set null values to an arbitrary value
print('wrangling data...')
for kanji in kanji_list:
    item = kanji_json[kanji]
    for category in categories:
        if not item[category]:
            item[category] = book[category]

    # make a new jlpt category (jlpt = 6 - jlpt_new)
    item["jlpt"] = 6 - item["jlpt_new"]

    # make a new wk category (wk = wk_level / 10)
    item["wk"] = item["wk_level"] / 10 + 1

    # delete categories to clean up data
    for category in filler:
        del item[category]

# dump the json to the output file
print('outputting data...')
# print(kanji_json)
pretty_json = json.dumps(kanji_json, indent=2, ensure_ascii=False).encode('utf8')
# print(pretty_json)
out_file.write(pretty_json.decode())

# close the files
print('closing files...')
json_file.close()
out_file.close()
