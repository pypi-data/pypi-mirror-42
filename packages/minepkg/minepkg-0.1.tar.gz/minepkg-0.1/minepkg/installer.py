import os
import subprocess
import tempfile

from tqdm import tqdm
import requests
import math

import minepkg.repository as repository


def install(pkgnames, alloptional, destination):
    install_list = set(pkgnames)

    repository.load()

    for pkgname in pkgnames:
        dependencies = _resove_dependencies(pkgname)
        for dep in dependencies:
            install_list.add(dep)

    if alloptional:
        for pkgname in pkgnames:
            dependencies = _resove_dependencies(pkgname, "dependencies_optional")
            for dep in dependencies:
                install_list.add(dep)

    print("Installing packages:")
    for package in install_list:
        print("- {}".format(package))
    print()
    print("Installing to {}".format(destination))

    while True:
        response = input("Continue installing? [Y/n]")
        if response == "" or response == "y" or response == "Y":
            break
        if response == "n" or response == "N":
            exit(0)

    with tempfile.TemporaryDirectory() as tempdir:
        for pkgname in install_list:
            _download(pkgname, tempdir)

        for pkgname in install_list:
            _extract(pkgname, tempdir, destination)
            with open(os.path.join(destination, pkgname, ".minepkgver"), "w") as handle:
                handle.write(repository.packages[pkgname]["version"])


def _download(pkgname, dir):
    url = repository.packages[pkgname]["source"]

    if url.startswith("https://github.com/"):
        url += "/archive/{}.tar.gz".format(repository.packages[pkgname]["version"])

    if url.startswith("https://gitlab.com/"):
        _, _, _, user, repo = url.split('/')
        rel = repository.packages[pkgname]["version"]
        url = 'https://gitlab.com/{user}/{repo}/-/archive/{rel}/{repo}-{rel}.tar.gz'.format(user=user, repo=repo,
                                                                                            rel=rel)

    target = os.path.join(dir, pkgname + '.tar.gz')

    r = requests.get(url, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0
    with open(target, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size // block_size), unit='KB',
                         unit_scale=True, desc=pkgname, dynamic_ncols=True):
            wrote = wrote + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")


def _extract(pkgname, tmpdir, destination):
    print("Installing {}...".format(pkgname))
    archive = os.path.join(tmpdir, pkgname + '.tar.gz')
    command = ['tar', '-tf', archive]
    files = subprocess.check_output(command, universal_newlines=True)

    roots = set()
    for file in files.splitlines():
        part = file.split('/')
        roots.add(part[0])

    if len(roots) > 1:
        raise Exception("tar archive has multiple root dirs, not supported yet")

    destination = os.path.join(destination, pkgname)
    os.mkdir(destination)

    command = ['tar', '-xf', archive, '--strip', '1', '--directory', destination]
    subprocess.check_output(command)


def _resove_dependencies(pkgname, depkey="dependencies"):
    if pkgname not in repository.packages:
        raise Exception("Package '{}' does not exist".format(pkgname))

    dependencies = set()

    for dep in repository.packages[pkgname][depkey]:
        dependencies.add(dep)
        for subdep in _resove_dependencies(dep):
            dependencies.add(subdep)

    return dependencies
