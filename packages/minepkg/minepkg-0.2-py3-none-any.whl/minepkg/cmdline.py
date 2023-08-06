import argparse
import os


def add(package, alloptional, destination):
    import minepkg.installer as installer

    if destination is None:
        if 'mods' in os.getcwd():
            destination = os.getcwd()

    if destination is None:
        destination = "~/.minetest/mods"

    destination = os.path.expanduser(destination)

    try:
        installer.install(package, alloptional, destination)
    except Exception as e:
        print(e)
        exit(1)


def update():
    import minepkg.repository
    minepkg.repository.update()


def makerepo(source, destination):
    import minepkg.makerepo

    minepkg.makerepo.make(source, destination)


def run():
    parser = argparse.ArgumentParser(description="A packagemanager for minetest")
    subparser = parser.add_subparsers(dest="subparser")

    parser_add = subparser.add_parser("add")
    parser_add.add_argument('package', help="Package name to install", nargs="+")
    parser_add.add_argument('--alloptional', '-a', help="Also install all optional dependencies", action="store_true")
    parser_add.add_argument('--destination', '-d', help="Destination directory for the mods")

    parser_update = subparser.add_parser("update")

    parser_makerepo = subparser.add_parser("makerepo")
    parser_makerepo.add_argument('source', help="Source directory")
    parser_makerepo.add_argument('destination', help="Output file")

    kwargs = vars(parser.parse_args())

    if kwargs['subparser'] is None:
        parser.print_usage()
        exit(1)

    globals()[kwargs.pop('subparser')](**kwargs)
