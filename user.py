import tkinter as tk
import os
import json
import urllib.request
import zipfile

# Init
path = os.path.dirname(os.path.abspath(__file__))
selfName = os.path.basename(__file__)
if selfName.endswith('.json'):
    isurl = True
    resourseUrl = selfName
else:
    isurl = False
    resourseUrl = None

# Self update
versionInfoUrl = 'https://raw.githubusercontent.com/wuyilingwei/Universal-online-mod-synchronizer/main/version.json'
version = 'v1.0.0'
build = 1
latestVersionStatus = 'Unknown'
with urllib.request.urlopen(versionInfoUrl) as url:
    data = json.loads(url.read().decode())
    print(f"Debug: Latest: {data}")
    if int(data['build']) > build:
        latestVersionStatus = 'Outdated'
        UpdateUrl = f'https://github.com/wuyilingwei/Universal-online-mod-synchronizer/releases/tag/{data["tag"]}'
        # Download and update
        print(f"Debug: Downloading from {UpdateUrl}")
        urllib.request.urlretrieve(UpdateUrl, os.path.join(path, selfName))
        print(f"Debug: Downloaded to {os.path.join(path, selfName)}")
        print(f"Debug: Restarting...")
        os.system(f'python {os.path.join(path, selfName)}')
        exit()
    else:
        latestVersionStatus = 'Latest'

print(f"Debug: path:{path} selfName:{selfName} isurl:{isurl}")

def getResourseInfo():
    resourseUrl = urlEntry.get()
    print(f"Debug: Getting info from {resourseUrl}")
    with urllib.request.urlopen(resourseUrl) as url:
        data = json.loads(url.read().decode())
        print(f"Debug: Info: {data}")
        for mod in data['mods']:
            print(f"Debug: Downloading {mod['name']} from {mod['url']}")
            urllib.request.urlretrieve(mod['url'], os.path.join(path, mod['name']))
            print(f"Debug: Downloaded to {os.path.join(path, mod['name'])}")
            with zipfile.ZipFile(os.path.join(path, mod['name']), 'r') as zip_ref:
                zip_ref.extractall(path)
            print(f"Debug: Extracted to {path}")
        print(f"Debug: Done")


root = tk.Tk()
root.title(f"Universal online mod synchronizer {version}")
root.geometry("400x200")
root.resizable(False, False)

if latestVersionStatus == 'Outdated':
    versionLabel = tk.Label(root, text=f"Program Version: {version} ({latestVersionStatus})", fg='red', anchor='w')
elif latestVersionStatus == 'Latest':
    versionLabel = tk.Label(root, text=f"Program Version: {version} ({latestVersionStatus})", fg='green', anchor='w')
else:
    versionLabel = tk.Label(root, text=f"Program Version: {version} Check failed", fg='yellow', anchor='w')
versionLabel.place(x=10, y=10, width=380, height=15)

urlLabel = tk.Label(root, text="Resource URL:", anchor='w')
urlLabel.place(x=10, y=30, width=180, height=15)
checkButton = tk.Button(root, text="Get Info", command=getResourseInfo)
if isurl:
    urlLabel = tk.Label(root, text=f"{selfName}", anchor='w')
    urlLabel.place(x=10, y=50, width=380, height=20, state=tk.DISABLED)
    getResourseInfo()
else:
    urlEntry = tk.Entry(root)
    urlEntry.place(x=10, y=50, width=380, height=20)

root.mainloop()