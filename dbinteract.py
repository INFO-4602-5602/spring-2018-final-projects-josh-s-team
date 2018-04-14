import pymysql
import configparser


class DillaDB:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("secrets.txt")
        self.user = config['MySQL']['user']
        self.pw = config['MySQL']['pw']
        self.db = config['MySQL']['db']
        db = pymysql.connect("localhost", self.user, self.pw, self.db)
        self.cursor = db.cursor()
        tables = self.cursor.execute("SHOW TABLES")
        print(tables)

    def checktables(self):
        tables = self.cursor.execute("SHOW TABLES")


    def addsong(self, title, year, dilla, pabit):
        print("addsong")
        # TODO: Implement
        # Query database for the max songID and save to a self variable
        # Then we can use that to know what the ID of the song is to link to artist

    def addartist(self, name):
        print("addartist")
        # TODO: Implement
        # Actually probably need to add the artist before the song, and then keep track of the artist ID

    def addlink(self, songid, sampledinid, sampledid):
        print("addlink")
        # TODO: Implement
        # Get the proper ids from editing the self value when adding songs/artists



