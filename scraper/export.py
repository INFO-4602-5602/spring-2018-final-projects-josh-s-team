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
            self.cursor.execute("DESCRIBE SampleExportDillaSongs")
            self.dillaSongCols = self.get_column_names(self.cursor.fetchall())
            self.cursor.execute("DESCRIBE SampleExportSampledSongs")
            self.sampledSongCols = self.get_column_names(self.cursor.fetchall())
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

    @staticmethod
    def get_column_names(info):
        names = list()
        for col in info:
            names.append(info[0])
        return names

    @staticmethod
    def songs_to_json(songlist, filename):
        print("Processing songs")
        objects_list = []
        for row in songlist:
            d = collections.OrderedDict()
            d['id'] = row[0]
            d['title'] = row[1]
            d['year'] = row[2]
            d['artist'] = row[8]
            d['producerid'] = row[4]
            d['genre'] = row[7]
            objects_list.append(d)

        j = json.dumps(objects_list)
        file = filename + ".json"
        f = open(file, 'w')
        print(j, file=f)

    @staticmethod
    def rels_to_json(rellist, filename):
        print("Processing relations")
        objects_list = []
        for row in rellist:
            d = collections.OrderedDict()
            d['song'] = row[0]
            d['sampled'] = row[1]
            objects_list.append(d)

        j = json.dumps(objects_list)
        file = filename + ".json"
        f = open(file, 'w')
        print(j, file=f)

    @staticmethod
    def add_dilla_rels(rels, dillasongs):
        for song in dillasongs:
            songid = song[0]
            link = (0, songid)
            rels = (link,) + rels
        return rels

    def export(self):
        print("Exporting...")
        self.cursor.execute("SELECT * FROM SampleExportDillaSongs")
        dillasongs = self.cursor.fetchall()
        self.songs_to_json(dillasongs, "dillasongs")
        self.cursor.execute("SELECT * FROM SampleExportSampledSongs")
        sampledsongs = self.cursor.fetchall()
        self.songs_to_json(sampledsongs, "sampledsongs")
        self.cursor.execute("SELECT song, sampled FROM SampleExportRel")
        rels = self.cursor.fetchall()
        rels = self.add_dilla_rels(rels, dillasongs)
        self.rels_to_json(rels, "rels")


if __name__ == "__main__":
    export = Export()
    export.export()
