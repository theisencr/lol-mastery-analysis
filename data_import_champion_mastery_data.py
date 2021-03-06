import sys, json, time
sys.dont_write_bytecode = True

from riot_api import RiotAPI

f = open("./api_key", "r")
api = RiotAPI(f.read())
f.close()

champion_graph_mapping = {}

f = open("./data/champion_list.csv","rU")

mapping_dict = {}
labelRow = False
for i in f:
  i = i.split(",")
  if(labelRow):
    mapping_dict[i[1]] = i[2]
  else:
    labelRow = True

f.close()

# affinity_dict = {}
# for x in range(0, 130):
#   affinity_dict[str(x)] = 0
#   for y in range(0, 130):
#     affinity_dict[str(x)][str(y)] = 0

f = open("./data/player_id_list.csv","rU")

w = open("./data/list_of_masteries.csv", "w")

w.write("graph_num,")
for x in range(0, 130):
  w.write(str(x) + ",")
w.write("\n")

w.write("0,")
notFirst = False
for x in range(0, 130):
  if (notFirst):
    w.write(",")
  w.write("0")
  notFirst = True
w.write("\n")

num_parsed = 0

for line in f:
  result = api.get_championmastery_playerid_allchampions(line.rstrip())
  player_dict = {}
  for i in result:
    #print str(i["championId"]) + "," + str(i["championLevel"])
    #print mapping_dict[line[0]]
    #print mapping_dict[str(i["championId"])]
    # affinity_dict[ mapping_dict[line.rstrip()]][ mapping_dict[str(i["championId"])] ] += int(i["championLevel"])
    #print mapping_dict[str(i["championId"])] + ": " + str(i["championLevel"])
    player_dict[mapping_dict[str(int(i["championId"]))]] = str(i["championLevel"])

  w.write(line.rstrip() + ",")
  notFirst = False
  for x in range(0, 130):
    if (notFirst):
      w.write(",")
    try:
      w.write(str(player_dict[str(x)]))
    except KeyError:
      w.write(str(0))
    notFirst = True
  w.write("\n")
  #respect the upper end of the rate limit on personal API keys...
  time.sleep(1.5)
  num_parsed += 1
  print("Number Parsed: " + str(num_parsed))