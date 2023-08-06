import os
import json
import glob


def make(source, destination):
    repository = {}
    search = os.path.join(os.path.abspath(source), "*.json")
    print("Searching {}".format(search))
    for sf in glob.glob(search):
        print(sf)
        with open(sf) as handle:
            data = json.loads(handle.read())

        name = os.path.basename(sf).replace(".json", "")
        repository[name] = data

    with open(destination, "w") as handle:
        handle.write(json.dumps(repository, indent=True))
