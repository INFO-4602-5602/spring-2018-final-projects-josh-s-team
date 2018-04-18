import requests
from bs4 import BeautifulSoup
import configparser
import re

baseURL = "https://www.whosampled.com/"
dillaURL = "https://www.whosampled.com/J-Dilla/"
dillaURL_paged = "https://www.whosampled.com/J-Dilla/?sp="
filetoggle = True


class Scraper:
    def __init__(self):
        print("Scraper init")
        self.url = dillaURL
        config = configparser.ConfigParser()
        config.read('secrets.txt')
        self.lastfmsecret = config['lastfm']['secret']
        self.lastfmapi = config['lastfm']['api']
        # Regex for splitting a song title from the year it was released
        self.titlere = re.compile('^(.+?)(?= \([0-9]{4}\))')
        if not filetoggle:
            try:
                self.soup = BeautifulSoup(requests.get(dillaURL), 'html.parser')
            except requests.exceptions.RequestException as e:
                print(e)

    @staticmethod
    def getnumpages(self):
        try:
            pages = self.soup.findAll('span',  {'class': 'page'})
            maxpages = pages[-1].string
            maxurl = pages[-1].a['href']
            print(maxpages)
            print(maxurl)

        except requests.exceptions.RequestException as e:
            print("Error! In getnumpages")
            print(e)

    @staticmethod
    def scrapesongs_url(self, pagenum):
        print("will we need this?")
        # Since whosampled.com hates being useful, they don't have an open API. I'm trying to get around this by using
        # bs4 and requests to just fetch the pages and scrape them; unfortunately they REALLY hate fun and noticed what
        # I was doing and rate limited the hell out of my IP / MAC address, I dunno how it works. I've resorted to
        # manually downloading all the pages and scraping them that way. If somehow we can get around the rate limit,
        # it would be pretty easy to convert from the scrapesongs_file function to this one
        # This is extra useful because we'd be able to open the actual page for a song's info, because I think the page
        # we're scraping from doesn't have all of the sample information on it, just 2 or 3 songs

    @staticmethod
    def process_artists(artistinfo):
        # Return dict object
        # {Artist:, Producer:, Features:}
        # Features is a list of names
        info = {
            "Artist": None,
            "Producer": None,
            "Features": list()
        }
        size = len(artistinfo)

        if size == 0:
            info['Artist'] = "J Dilla"
            info['Producer'] = 'J Dilla'
        elif size == 1:
            feats = artistinfo[0].find_all('a')
            info['Artist'] = feats[0].getText()
            for artist in feats[1:]:
                artist = artist.getText()
                if artist == "J Dilla":
                    info["Producer"] = "J Dilla"
                else:
                    info['Features'].append(artist)
                    info['Producer'] = "J Dilla"
        elif size == 2:
            info['Artist'] = artistinfo[0].find('a').getText()
            info['Producer'] = artistinfo[1].find('a').getText()

        return info

    def process_samples(self, sampleinfo):
        connections = sampleinfo.find_all('div', {'class': 'track-connection'})
        samplelist = list()
        for connection in connections:
            if connection.find('span', {'class': 'sampleAction'}).getText().strip(" \n\t") != "sampled":
                continue
            else:
                samples = connection.find_all("li")
                for sample in samples:
                    song = sample.text.strip(" \n\t").replace('\t', '').split('\n')
                    title = song[0]
                    info = song[1][3:]
                    artistspan = self.titlere.match(info).span()
                    artist = info[artistspan[0]:artistspan[1]].split('feat.')[0]
                    year = info[artistspan[1]:].strip(' ()')
                    sampledinfo = {
                        'Title': title,
                        'Artist': artist,
                        'Year': year,
                        'Genre': self.get_genre(title, artist)
                    }
                    samplelist.append(sampledinfo)
        return samplelist

    def get_genre(self, song, artist):
        url = "https://ws.audioscrobbler.com/2.0/?method=track.gettoptags&artist={}&track={}" \
              "&api_key={}&format=json&autocorrect=1".format(artist.replace(" ", "+"),
                                                             song.replace(" ", "+"), self.lastfmapi)
        try:
            response = requests.get(url)
            if response.status_code != 200 or 'error' in response.json():
                genre = None
                return genre
            else:
                tags = response.json()['toptags']['tag']
                if len(tags) == 0:
                    genre = None
                else:
                    genre = tags[0]['name'].lower()
            return genre
        except requests.exceptions.RequestException as e:
            print(e)

    def scrapesongs_file(self, pagenum):
        # Return a list of dict items
        # {Title:, Year:, Artist:, Producer:, Features:, Sampled:}
        # Features and Samples are lists
        items = list()
        filename = "dilla" + str(pagenum)
        path = "pages/" + filename + ".html"
        soup = BeautifulSoup(open(path), "html.parser")
        for song in soup.find_all('article', {'class': 'trackItem'}):
            track = song.find('header', {'class': 'trackItemHead'})
            path = track.find('a', {'itemprop': 'sameAs'}, href=True)['href']
            title = track.find('a', {'itemprop': 'sameAs'}).getText()
            year = track.find('span', {'class': 'trackYear'}).getText().strip(' ()')
            artist = track.find_all('span', {'class': 'trackArtistName'})
            samples = song.find('div', {'class': 'trackConnections'})

            trackinfo = self.process_artists(artist)
            sampleinfo = self.process_samples(samples)

            info = {
                'Title': title,
                'Year': year,
                'Artist': trackinfo['Artist'],
                'Producer': trackinfo['Producer'],
                'Features': trackinfo['Features'],
                'Sampled': sampleinfo,
                'Genre': self.get_genre(str(title), str(trackinfo['Artist']))
            }

            items.append(info)
            print(info)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return items


if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrapesongs_file(6)
