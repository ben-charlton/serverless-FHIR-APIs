#!/usr/bin/python
import json
from functools import cmp_to_key

u_list = [
{
    "linkId": "1.1",
    "text": "innner item 1"
},
{
    "linkId": "2",
    "text": "outer item 2"
},
{
    "linkId": "1",
    "text": "outer item 1"
},
{
    "linkId": "2.1",
    "text": "inner item 2"
},
{
    "linkId": "2.1.1",
    "text": "inner inner item 2"
}]

for entry in u_list:
  entry["sortid"] = (entry["linkId"]).replace('.','')
  entry["items"] = []

def compare(item1, item2):
        if item1["linkId"] < item2["linkId"]:
            return -1
        elif item1["linkId"] > item2["linkId"]:
            return 1
        else:
            return 0

s_list = sorted(u_list, key=cmp_to_key(compare))

maxNesting = 0
for entry in u_list:
  nesting = len(entry["sortid"])
  if nesting > maxNesting:
    maxNesting = nesting

while maxNesting > 1:
  itemIndex = 0
  while itemIndex < len(s_list):
    if ("sortid" in s_list[itemIndex]) and (len(s_list[itemIndex]["sortid"]) == maxNesting):
      innerIndex = 0
      while innerIndex < len(s_list):
        if ("sortid" in s_list[innerIndex]) and (len(s_list[innerIndex]["sortid"]) == maxNesting -1) :
          s1 = s_list[innerIndex]["sortid"]
          s2 = s_list[itemIndex]["sortid"][:-1]
          if (s1 == s2) :
            del s_list[itemIndex]["sortid"]
            s_list[innerIndex]["items"].append(s_list[itemIndex])
            break
        innerIndex += 1
    itemIndex +=1
  maxNesting -= 1

s_list = [x for x in s_list if "sortid" in x]
for entry in s_list:
  del entry["sortid"]

print("------------------------------")
print(json.dumps(s_list, indent=4))



