import argparse
import os

from frisk import Frisk
from frisk.settings import VERSION

if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(description='Frisk - Simple duplicate detector.')
    arg_parser.add_argument('--version', action='version', version='Frisk v{}'.format(VERSION))
    arg_parser.add_argument('initial_path', type=str, nargs='*',
        help="""The base folder from which to scan, looking for duplicates in it and subfolders.
        If multiple folders are, all will be scanned.""")
    arg_parser.add_argument('--check-file', '-c', type=str, dest='check_file',
        help="Check a single file against the database.")
    arg_parser.add_argument('--check-name', '-cn', type=str, dest='check_name',
        help="Check the name of a file against the database, if it exists it will return it's location.")

    args = arg_parser.parse_args()

    if args.initial_path:
        for path in args.initial_path:
            if os.path.exists(path):
                print(path)
                #frisk = Frisk(base_folder=args.initial_path)
                #frisk.run()
            else:
                print("Invalid path - {}".format(path))
    elif args.check_file:
        if os.path.exists(args.check_file):
            print(args.check_file)
            #frisk = Frisk(single_file=args.check_file)
            #frisk.run()
        else:
            print("Invalid path - {}".format(args.check_file))
    elif args.check_name:
        frisk = Frisk(single_name=args.check_name)
        result = frisk.run()
        print(result)
