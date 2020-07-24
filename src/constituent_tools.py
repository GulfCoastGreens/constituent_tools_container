#!/usr/bin/env python
import sys
import argparse
from georgia.georgia import georgia
from florida.florida import florida
from vtconnection import vtconnection

def main(args):
    if args.state:
        if args.state == 'florida':
            fl = florida(args,vtconnection(args))
            fl.info()
        elif args.state == 'georgia':
            georgia = georgia(args,vtconnection(args))
            georgia.info()
        else:
            print("Error: a valid state must be specified")
    else:
        print("A state must be specified with --state")
# for arg in sys.argv:
#    print(arg)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", help="Indicate the state")
    parser.add_argument("--action", help="Indicate the process action")
    parser.add_argument("--type", help="Indicate the process type")
    # args = parser.parse_args()
    main(parser.parse_args())