# Wrangle a JSON database to suit website needs
# original data from https://github.com/davidluzgouveia/kanji-data
# hyogai and jinmeiyo extension from https://github.com/mifunetoshiro/kanjium/blob/master/data/kanjidb.sqlite
import json

# Open the JSON file
print('setting up files...')
file_name = "kanji-jouyou.json"
json_file = open(file_name, 'r')

# Set up output file
out_file = open("kanji_5.json", 'w')

# Load the file into a JSON object
print('setting up json...')
kanji_json = json.load(json_file)

############################################################
# NEW version 1.2 (reformatting kanji grade list)
# SOURCES:
# https://www.kanji-link.com/en/kanji/grade/
# https://www.kanshudo.com/collections/jlpt_kanji
# had to replace two more kanji to conform to 2010 standards
############################################################
# open up list file
print('adjusting grade levels...')
list_file_name = 'kanji_grade_list.txt'
list_file = open(list_file_name, 'r')

kanji_string = list_file.readline().replace(' ', '').strip('\n')
count = 1

# adjust grade levels
while kanji_string:
    for kanji in kanji_string:
        kanji_json[kanji]["grade"] = count
    kanji_string = list_file.readline().replace(' ', '').strip('\n')
    count += 1

list_file.close()

# jlpt adjust
jlpt_file_name = 'kanji_jlpt.txt'
jlpt_file = open(jlpt_file_name, 'r')

kanji_list = [kanji for kanji, _ in kanji_json.items()]
for kanji in kanji_list:
    kanji_json[kanji]["jlpt_new"] = 1

kanji_string = jlpt_file.readline().replace(' ', '').strip('\n')
count = 5

while count > 1:
    for kanji in kanji_string:
        kanji_json[kanji]["jlpt_new"] = count
    kanji_string = jlpt_file.readline().replace(' ', '').strip('\n')
    count -= 1

jlpt_file.close()

# shinjitai kanji
confusion = ['叱', '𠮟', '剥', '剝']
kanji_json[confusion[1]] = kanji_json[confusion[0]].copy()
kanji_json[confusion[3]] = kanji_json[confusion[2]].copy()
kanji_json[confusion[1]]['wk_level'] = None

############################################################

# make a new kanji list
kanji_list = [kanji for kanji, _ in kanji_json.items()]

# setup categories
categories = ["freq", "jlpt_new", "wk_level"]
filler = ["jlpt_old", "jlpt_new", "meanings", "readings_on", "readings_kun",
          "wk_level", "wk_meanings", "wk_readings_on", "wk_readings_kun", "wk_radicals"]

# set new values if null
book = dict()
book["freq"] = 2500
book["jlpt_new"] = 1
book["wk_level"] = 61

# modify the JSON data
print('wrangling data...')
for kanji in kanji_list:
    item = kanji_json[kanji]

    # set null values to an arbitrary value
    for category in categories:
        if not item[category]:
            item[category] = book[category]

    # make a new jlpt category (jlpt = 6 - jlpt_new)
    item["jlpt"] = 6 - item["jlpt_new"]

    # make a new wk category (wk = wk_level / 10)
    item["wk"] = item["wk_level"] / 10

    # delete categories to clean up data
    for category in filler:
        del item[category]


############################################################
# NEW version 1.1 (adding jinmeiyo and hyogai kanji)
############################################################
def fill_in_kanji(source, destination, grade, jlpt, wk):
    for obj in source:
        kanji = obj['kanji']
        try:
            print(destination[kanji], kanji)
        except KeyError:
            destination[kanji] = {}
            destination[kanji]["grade"] = grade
            destination[kanji]["jlpt"] = jlpt
            destination[kanji]["wk"] = wk


jinmeiyo_name = "kanji-jinmeiyo.json"
jinmeiyo_file = open(jinmeiyo_name, 'r')
jinmeiyo_json = json.load(jinmeiyo_file)

hyogai_name = "kanji-hyogai.json"
hyogai_file = open(hyogai_name, 'r')
hyogai_json = json.load(hyogai_file)

fill_in_kanji(hyogai_json, kanji_json, 9, 6, 7)
fill_in_kanji(jinmeiyo_json, kanji_json, 10, 7, 8)

############################################################

# dump the json to the output file
# make sure to keep kanji in their original form
# doing dumps normally with pretty print will print them as unicode!!
print('outputting data...')
pretty_json = json.dumps(kanji_json, indent=2, ensure_ascii=False).encode('utf8')
out_file.write(pretty_json.decode())

# close the files
print('closing files...')
json_file.close()
jinmeiyo_file.close()
hyogai_file.close()
out_file.close()
