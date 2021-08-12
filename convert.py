# Convert a JSON file to CSV
import json

# Open the JSON file
file_name = "kanji-jouyou.json"
json_file = open(file_name, 'r')

# Set up output file
output = open("kanji.csv", 'w')

# Load the file into a JSON object
json = json.load(json_file)
kanji_list = [kanji for kanji, _ in json.items()]

# print header row to csv
categories = ["strokes", "grade", "freq", "jlpt_new", "wk_level"]
header = "char"
for category in categories:
    header += f",{category}"
output.write(f"{header}\n")

# print file to csv
for kanji in kanji_list:
    row = f"{kanji}"
    item = json[kanji]

    for category in categories:
        row += f",{item[category]}"

    output.write(f"{row}\n")
    # print(f"{row}")


# close the files
json_file.close()
output.close()
