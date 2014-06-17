import argparse
import os

from frisk import Frisk

if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(description='Frisk - Duplicate detector.')
    arg_parser.add_argument('initial_path', type=str,
        help='The base folder from which to scan, looking for duplicates in it and subfolders.')

    args = arg_parser.parse_args()

    if args.initial_path:
        if os.path.exists(args.initial_path):
            print(args.initial_path)
            #frisk = Frisk(args.initial_path)
            #frisk.run()
        else:
            print("Invalid path.")
