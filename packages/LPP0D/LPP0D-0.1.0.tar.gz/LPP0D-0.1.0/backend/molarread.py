import json as js

li = []
with open('molar_masses.txt', 'r') as f:
  for l in f.readlines():
     li.append((l.split()[0].strip(), eval(l.split()[1].strip())))
molardic = dict(li) 
