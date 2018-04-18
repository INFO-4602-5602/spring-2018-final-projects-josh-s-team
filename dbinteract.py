import pymysql
import configparser

dillanames = ("J Dilla", "Jay Dee")


class DillaDB:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("secrets.txt")
        self.user = config['MySQL']['user']
        self.pw = config['MySQL']['pw']
        self.db = config['MySQL']['db']
        self.artists = {}
        try:
            connection = pymysql.connect("localhost", self.user, self.pw, self.db)
            connection.set_charset('utf8')
            connection.autocommit(True)
            self.cursor = connection.cursor()
            self.cursor.execute('SET NAMES utf8;')
            self.cursor.execute('SET CHARACTER SET utf8;')
            self.cursor.execute('SET character_set_connection=utf8;')
            self.cursor.execute("SHOW TABLES;")
            if len(self.cursor.fetchall()) != 4:
                print("Error! MySQL tables not initialized.\nLog into your favorite mysql platform as root at "
                      "localhost, then run the createdb.sql script.\nThis will create the appropriate user and "
                      "tables to be used. Then, rerun this initialization. How'd you do this, anyway?")
        except pymysql.err.OperationalError or pymysql.err.InternalError as e:
            if e.args[0] == 1045:
                print("Error! User or database is not initialized.\nLog into your favorite mysql platform as root "
                      "at localhost, then run the createdb.sql script.\nThis will create the appropriate "
                      "user and tables to be used.")
                print("\n")
                print(e)
                exit(1)

    def addsong(self, title, year, dilla, pabit, artistid, prodid, genre):
        cmd = 'INSERT INTO Songs (Title, ReleaseYear, Artist, Producer, DillaBit, PABit, Genre) VALUES ' \
              '(\'{}\',{},{},{},{},{},\'{}\');'.format(title.replace("'", "\\'"), year, artistid, prodid, dilla, pabit, genre)
        self.cursor.execute(cmd)
        return self.cursor.lastrowid

    def addartist(self, name):
        cmd = 'INSERT IGNORE INTO Artists (Name) VALUE ("{}")'.format(name)
        self.cursor.execute(cmd)
        artistid = self.cursor.lastrowid
        if artistid != 0 and artistid not in self.artists:
            self.artists.update({name: artistid})

    def addlink(self, songid, sampleid):
        cmd = 'INSERT INTO Rel (Song, Sampled) VALUES ({},{});'.format(songid, sampleid)
        self.cursor.execute(cmd)

    def addsample(self, sampleinfo):
        artist = sampleinfo['Artist'].replace("'", "\\'").replace('"', '\\"').strip(' ')
        title = sampleinfo['Title'].replace("'", "\\'").replace('"', '\\"').strip(' ')
        year = sampleinfo['Year']
        genre = sampleinfo['Genre']
        self.addartist(artist)
        artistid = self.artists[artist]
        cmd = 'INSERT INTO Songs (Title, ReleaseYear, Artist, DillaBit, Genre) VALUES ' \
              '(\'{}\',{},{},{},\'{}\');'.format(title, year, artistid, 0, genre)
        self.cursor.execute(cmd)
        return self.cursor.lastrowid

    def addinfo(self, songinfo):
        print(songinfo)
        title = songinfo['Title']
        year = songinfo['Year']
        artist = songinfo['Artist'].replace("'", "\\'").replace('"', '\\"')
        prod = songinfo['Producer']
        genre = songinfo['Genre']
        features = songinfo['Features']
        samples = list()

        if prod in dillanames or artist in dillanames:
            dilla = 1
        else:
            dilla = 0
        # If artist/producer is J Dilla, pabit = 1
        # If just producer pabit = 0
        # I think? I'll need to check my notes
        if artist in dillanames:
            pabit = 1
        else:
            pabit = 0

        self.addartist(artist)
        self.addartist(prod)
        artistid = self.artists[artist]
        prodid = self.artists[prod]

        for feat in features:
            self.addartist(feat)

        for sample in songinfo['Sampled']:
            samples.append(self.addsample(sample))

        songid = self.addsong(title, year, dilla, pabit, artistid, prodid, genre)

        for sampleid in samples:
            self.addlink(songid, sampleid)

        print("Song added!")

    def __exit__(self):
        self.cursor.close()


if __name__ == "__main__":
    db = DillaDB()
