from .importvoters import ImportVoters
from .importhistory import ImportHistories

class florida:
    _connection = None
    _cursor = None
    def __init__(self, args, db):
        self.args = args
        if args.action:
            if args.action == 'import':
                print("Import")
                if args.type:
                    if args.type == 'voter':
                        self.importvoters = ImportVoters(args,db)
                        self.importvoters.iterateZip()
                    elif args.type == 'history':
                        self.importhistory = ImportHistories(args,db)
                else:
                    print("A type must be specified with --type")
                # florida = Florida(args)
                # florida.info()
            elif args.action == 'export':
                print("Export")
                # georgia = Georgia(args)
                # georgia.info()
            else:
                print("Error: a valid action must be specified")
        else:
            print("A action must be specified with --action")

    def info(self):
        print("State set to Florida")

