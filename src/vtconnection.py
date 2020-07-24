import os
import psycopg2

class vtconnection:
    _connection = None
    _cursor = None
    def __init__(self, args):
        self.args = args
        print("Invoked Connection")
        self.setConnection()
    def setConnection(self):
        try:
            self._connection = psycopg2.connect(user = os.getenv('PG_USER'),
                                        password = os.getenv('PG_PASSWORD'),
                                        host = os.getenv('PG_HOST'),
                                        port = os.getenv('PG_PORT'),
                                        database = os.getenv('usvoters'))

            self._cursor = self._connection.cursor()
            # Print PostgreSQL Connection properties
            # print ( self._connection.get_dsn_parameters(),"\n")

            # Print PostgreSQL version
            self._cursor.execute("SELECT version();")
            # record = self._cursor.fetchone()
            # print("You are connected to - ", record,"\n")

        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
    def getConnection(self):
        return self._connection
    def close(self):
        #closing database connection.
        if(self._connection):
            self._cursor.close()
            self._connection.close()
            print("PostgreSQL connection is closed")
