import pymysql
import configparser
import collections
import json


class Export:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("secrets.txt")
        self.user = config['MySQL']['user']
        self.pw = config['MySQL']['pw']
        self.db = config['MySQL']['db']
        try:
            connection = pymysql.connect("localhost", self.user, self.pw, self.db)
            connection.set_charset('utf8')
            connection.autocommit(True)
            self.cursor = connection.cursor()
            # self.cursor.execute('source prepare.sql')
            self.cursor.execute("SHOW TABLES;")
            if len(self.cursor.fetchall()) != 8:
                print("Error! It looks like all the tables aren't there.\n Try logging into your favorite MySQL client"
                      "as root at localhost and executing the prepare.sql script. This should get everything ready"
                      "for exporting. At least for the test. I think.\n")
            self.cursor.execute("DESCRIBE SampleExportSongs")
            self.songCols = self.get_column_names(self.cursor.fetchall())
            self.cursor.execute("DESCRIBE SampleExportArtists")
            self.artistCols = self.get_column_names(self.cursor.fetchall())
            self.cursor.execute("DESCRIBE SampleExportRel")
            self.relCols = self.get_column_names(self.cursor.fetchall())
        except pymysql.err.OperationalError as e:
            print("Error! Couldn't connect to MySQL database\n")
            print(e)
            exit(1)
        except pymysql.err.ProgrammingError as e:
            print("Ah the syntax is wrong. Whoops.\n")
            print(e)
            exit(1)

    def get_column_names(self, info):
        names = list()
        for col in info:
            names.append(info[0])
        return names

    def artists_to_json(self, list):
        print("Processing artists")
        objects_list = []
        for row in list:
            d = collections.OrderedDict()
            d['id'] = row[0]
            d['name'] = row[1]
            objects_list.append(d)

        j = json.dumps(objects_list)
        file = 'testArtists.json'
        f = open(file, 'w')
        print(j, file=f)

    def songs_to_json(self, list):
        print("Processing songs")
        objects_list = []
        for row in list:
            d = collections.OrderedDict()
            d['id'] = row[0]
            d['title'] = row[1]
            d['year'] = row[2]
            d['artistid'] = row[3]
            d['producerid'] = row[4]
            d['dilla'] = row[5]
            d['genre'] = row[7]
            objects_list.append(d)

        j = json.dumps(objects_list)
        file = 'testSongs.json'
        f = open(file, 'w')
        print(j, file=f)

    def rels_to_json(self, list):
        print("Processing relations")
        objects_list = []
        for row in list:
            d = collections.OrderedDict()
            d['id'] = row[0]
            d['song'] = row[1]
            d['sampled'] = row[2]
            objects_list.append(d)

        j = json.dumps(objects_list)
        file = 'testRel.json'
        f = open(file, 'w')
        print(j, file=f)

    def export(self):
        print("Exporting...")
        self.cursor.execute("SELECT * FROM SampleExportSongs")
        songs = self.cursor.fetchall()
        self.songs_to_json(songs)
        self.cursor.execute("SELECT * FROM SampleExportArtists")
        artists = self.cursor.fetchall()
        self.artists_to_json(artists)
        self.cursor.execute("SELECT * FROM SampleExportRel")
        rels = self.cursor.fetchall()
        self.rels_to_json(rels)


if __name__ == "__main__":
    export = Export()
    export.export()
