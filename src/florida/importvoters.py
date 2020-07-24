import os
import csv
from datetime import datetime
from datetime import date
import psycopg2
import psycopg2.extras
from io import BytesIO
from zipfile import ZipFile

class ImportVoters:
    _connection = None
    _cursor = None
    _state = "FL"
    _fields = [
        'county_code',
        'id',
        'name_last',
        'name_suffix',
        'name_first',
        'name_middle',
        'exemption',
        'residential_address_line_1',
        'residential_address_line_2',
        'residential_city',
        'residential_state',
        'residential_zipcode',
        'mailing_address_line_1',
        'mailing_address_line_2',
        'mailing_address_line_3',
        'mailing_city',
        'mailing_state',
        'mailing_zipcode',
        'mailing_country',
        'gender',
        'race',
        'birth_date',
        'registration_date',
        'party_affiliation',
        'precinct',
        'precinct_group',
        'precinct_split',
        'precinct_suffix',
        'voter_status',
        'congressional_district',
        'house_district',
        'senate_district',
        'county_commission_district',
        'school_board_district',
        'daytime_areacode',
        'daytime_phone',
        'daytime_phone_extension',
        'email',
        'export_date'
    ]
    def __init__(self, args, db):
        self.args = args
        print("Invoked ImportVoters")
        self.db = db
        self._connection = self.db.getConnection()
        # self._connection.set_session(autocommit=True)
        # self._connection.autocommit = True
        # self._cursor = self.db.getConnection().cursor()
    def createstagingtable(self,cursor) -> None:
        with open(os.path.join(os.path.dirname(__file__),"sql/SetupVoterImport.sql")) as sqlscript:
            cursor.execute(sqlscript.read())
    # def importByCounty(self):

    def iterateZip(self):
        with self._connection as conn:
            with conn.cursor() as cursor:
                self.createstagingtable(cursor)
        # self._connection.commit()
        # print(os.path.dirname(__file__))
        # print(os.path.join(os.path.dirname(__file__),"sql/SetupVoterImport.sql"))
        # with open(os.path.join(os.path.dirname(__file__),"sql/SetupVoterImport.sql")) as sqlscript:
        #     # print(sqlscript.read())
        #     self._cursor.execute(sqlscript.read())
        #     self._connection.commit()
        # sql_file = open('florida/sql/SetupVoterImport.sql','r')
        # with open(os.path.join(os.path.dirname(__file__), "/sql/SetupVoterImport.sql"),'r') as sql_file:            
        #     print(sql_file.read())
            # self._cursor.execute(sql_file.read())
        voterfileinfo = None
        export_date = None
        with ZipFile('/data/VoterExtract.zip') as voterfile:
            with open(("/data/voter_tmp.txt"), "wb") as output:
                for county_file in voterfile.namelist():
                    if voterfileinfo == None:
                        voterfileinfo = voterfile.getinfo(county_file)
                        print(voterfileinfo.date_time)
                        # dt_obj = datetime(voterfileinfo.date_time)
                        # print(dt_obj)
                        # voterfileinfo.date_time[0] # Year (>= 1980)
                        # voterfileinfo.date_time[1] # Month (one-based)
                        # voterfileinfo.date_time[2] # Day of month (one-based)
                        export_date = '/'.join([
                            str(voterfileinfo.date_time[1]).zfill(2),
                            str(voterfileinfo.date_time[2]).zfill(2),
                            str(voterfileinfo.date_time[0])
                        ])
                    # for line in voterfile.open(county_file).readlines():
                    #     if len(line.decode("utf-8").split("\t")) == 38:
                    #         output.write(line)
            # with open(("/data/voter_tmp.txt"), "r",encoding="utf-8") as output:
            #     reader = csv.DictReader(output,fieldnames=self._fields,delimiter="\t")
            #     with self._connection as conn:
            #         with conn.cursor() as cursor:
            #             psycopg2.extras.execute_values(cursor, """
            #                 INSERT INTO public.voter VALUES %s
            #                 ON CONFLICT ON CONSTRAINT voter_pk 
            #                 DO NOTHING;
            #             """, (( 
            #                 row['county_code'][:3],
            #                 row['id'][:10],
            #                 row['name_last'][:30],
            #                 row['name_suffix'][:5],
            #                 row['name_first'][:30],
            #                 row['name_middle'][:30],
            #                 row['exemption'][:1],
            #                 row['residential_address_line_1'][:50],
            #                 row['residential_address_line_2'][:40],
            #                 row['residential_city'][:40],
            #                 row['residential_state'][:2],
            #                 row['residential_zipcode'][:10],
            #                 row['mailing_address_line_1'][:40],
            #                 row['mailing_address_line_2'][:40],
            #                 row['mailing_address_line_3'][:40],
            #                 row['mailing_city'][:40],
            #                 row['mailing_state'][:2],
            #                 row['mailing_zipcode'][:12],
            #                 row['mailing_country'][:40],
            #                 row['gender'][:1],
            #                 row['race'][:1],
            #                 self.convertImportDate(row['birth_date'][:10]),
            #                 self.convertImportDate(row['registration_date'][:10]),
            #                 row['party_affiliation'][:3],
            #                 row['precinct'][:6],
            #                 row['precinct_group'][:3],
            #                 row['precinct_split'][:6],
            #                 row['precinct_suffix'][:3],
            #                 row['voter_status'][:3],
            #                 row['congressional_district'][:3],
            #                 row['house_district'][:3],
            #                 row['senate_district'][:3],
            #                 row['county_commission_district'][:3],
            #                 row['school_board_district'][:2],
            #                 row['daytime_areacode'][:3],
            #                 row['daytime_phone'][:7],
            #                 row['daytime_phone_extension'][:4],
            #                 row['email'][:100],
            #                 self.convertImportDate(export_date)
            #             ) for row in reader ))
            self.getMetadata(export_date)
                
    def convertImportDate(self,datestr):
        try:
            date_obj = datetime.strptime(datestr, '%m/%d/%Y')
        except ValueError as err:
            print('ValueError Raised:', err)
            # raise ValueError('The time must have the format MM/DD/YYYY')
            return None
        else:
            return date_obj.date()

    # def registerIdentifier(self,identifier):
    #     with self._connection.cursor() as cursor:

    #         self._state
    def createIdentity(self,cursor):
        cursor.execute("""INSERT INTO identity DEFAULT VALUES RETURNING id""")
        return cursor.fetchone()[0]

    def getIdentifier(self,cursor,identifier):
        cursor.execute(""" 
          select * from public.identifier where identifier=%s and state_id=%s
        """,(identifier,self._state))
        return cursor.fetchall()

    def setIdentifier(self,cursor,identifier,identity):
        cursor.execute(""" 
          INSERT INTO public.identifier (identity_id,identifier,state_id) VALUES (%s,%s,%s)
        """,(identity,identifier,self._state) )
        return self.getIdentifier(cursor,identifier)

    def getMetadata(self,export_date):
        with self._connection as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(""" 
                    SELECT county_code,id,party_affiliation,export_date FROM public.voter WHERE export_date=%s 
                """, (self.convertImportDate(export_date),))
                for row in cursor.fetchall():
                    with conn.cursor() as icursor:
                        # print(row['id'])
                        identifiers = self.getIdentifier(icursor,row['id'])
                        if len(identifiers) < 1:
                            # print(identifiers)
                            with conn.cursor() as idcursor:
                                identityId = self.createIdentity(idcursor)
                                # print(identityId)
                                identifiers = self.setIdentifier(icursor,row['id'],identityId)
                    with conn.cursor() as icursor:
                        icursor.execute(""" 
                            INSERT INTO public.party_history (county_code,voter_id,party_affiliation,export_date) VALUES(%s,%s,%s,%s)
                            ON CONFLICT ON CONSTRAINT party_history_pkey 
                            DO NOTHING;
                        """, (row['county_code'],row['id'],row['party_affiliation'],row['export_date']) )
