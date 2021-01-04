import json

result = {}

with open("data/entry_correlations.csv") as in_file:
   header = in_file.readline()
   entry_ids = list(map(lambda a: a.strip(), header.split(',')))
   print(entry_ids)
   for x, line in enumerate(in_file):
    corrs = list(map(lambda a: a.strip(), line.split(',')))
    result[entry_ids[x]] = {}
    for y, corr in enumerate(corrs):
      if corr != '':
        result[entry_ids[x]][entry_ids[y]] = float(corr)

json_result = json.dumps(result, indent=4)

with open("data/correlations.json", "w") as text_file:
    text_file.write(json_result)

