import tkinter as tk
import os
import json
import urllib.request

# Init
path = os.path.dirname(os.path.abspath(__file__))
selfname = os.path.basename(__file__)
if selfname.endswith('.json'):
    isurl = True
else:
    isurl = False

# Self update
# URL
if isurl:
    with urllib.request.urlopen(selfname) as response:
        data = response.read()
        with open(f"{path}/newest.json", "wb") as f:
            f.write(data)
    with open(f"{path}/newest.json", "r") as f:
        newest = json.load(f)


print(f"Debug: path:{path} selfname:{selfname} isurl:{isurl}")