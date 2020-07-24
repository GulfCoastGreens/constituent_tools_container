
class ImportHistories:
    _connection = None
    _cursor = None
    def __init__(self, args, db):
        self.args = args
        print("Invoked ImportHistories")
        self.db = db
        self._connection = self.db.getConnection()
        self._cursor = self.db.getConnection().cursor()
