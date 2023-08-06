import math
import os
import json

import requests
import xdg.BaseDirectory
from tqdm import tqdm

path = os.path.join(xdg.BaseDirectory.xdg_cache_home, 'minepkg.json')

packages = {}


def load():
    global path, packages

    if packages != {}:
        return

    if not os.path.isfile(path):
        print("Not found: {}".format(path))

    if os.path.isfile("repository.json"):
        path = "repository.json"

    with open(path, 'r') as handle:
        raw = handle.read()

    packages = json.loads(raw)


def _download(url, target):
    r = requests.get(url, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0
    with open(target, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size // block_size), unit='KB',
                         unit_scale=True, desc="packages.json", dynamic_ncols=True):
            wrote = wrote + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")


def update():
    downdir = os.path.dirname(path)
    os.makedirs(downdir, exist_ok=True)
    _download("https://minepkg.brixit.nl/repository.json", path)
