import json

# load tank definitions
f = open("./tank_definitions.json")
DEFINITIONS = json.load(f)
f.close()

