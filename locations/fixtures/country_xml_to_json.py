import codecs
import string
import json
import re

f = codecs.open("country_names_and_codes.txt", encoding="utf-8")

countries = []
for idx, line in enumerate(f):
	s = line.strip() # remove EOL
	name, code_alpha2, code_alpha3, code_numeric = re.compile("\ \s+|\t\s*").split(s)

	country = {
		"pk": idx,
		"model": "locations.country",
		"fields": {
			"name": string.capwords(name),
			"type": "1",
			"code_alpha2": code_alpha2,
			"code_alpha3": code_alpha3,
			"code_numeric": code_numeric,
		}
	}
	countries.append(country)

print json.dumps(countries, sort_keys=True, indent=4)
