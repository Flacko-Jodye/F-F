import json

data = json.load(open('C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/Netzwerke1/Vorlage_Projekt_Netzwerke/Data/chvatal_small.json'))

# s und t festlegen
data['nodes']['source'] = {'demand': 0}
data['nodes']['target'] = {'demand': 0}

# Umbenennen der Arcs
#   upper bound der arcs werden zum flow

for arc in data["arcs"]:
    arc["arc_flow"] = arc["upper_bound"]

for node, x in data['nodes'].items():
    if x['demand'] < 0:
        data['arcs'].append({
            "from": "source",
            "to": node,
            "cost": 0,
            "lower_bound": 0,
            "arc_flow": abs(x['demand'])
        })
    elif x['demand'] > 0:
        data['arcs'].append({
            "from": node,
            "to": "target",
            "cost": 0,
            "lower_bound": 0,
            "arc_flow": abs(x['demand'])
        })

# Transformierte Daten speichern
with open('C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/chvatal_small_transformed_v2.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)