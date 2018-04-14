import requests
from bs4 import BeautifulSoup

baseURL = "https://www.whosampled.com/"
dillaURL = "https://www.whosampled.com/J-Dilla/"
dillaURL_paged = "https://www.whosampled.com/J-Dilla/?sp="
filetoggle = True


class Scraper:
    def __init__(self):
        print("Scraper init")
        self.url = dillaURL
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
        elif size == 2:
            info['Artist'] = artistinfo[0].find('a').getText()
            info['Producer'] = artistinfo[1].find('a').getText()

        return info

    def scrapesongs_file(self, pagenum):
        # Return a dict
        # {Title:, Year:, Artist:, Producer:, Features:,
        # SampledIn:, Sampled:}
        # Features, SampledIn, and Samples are lists
        filename = "dilla" + str(pagenum)
        path = "pages/" + filename + ".html"
        soup = BeautifulSoup(open(path), "html.parser")
        for song in soup.find_all('article', {'class': 'trackItem'}):
            track = song.find('header', {'class': 'trackItemHead'})
            title = track.find('a', {'itemprop': 'sameAs'}).getText()
            year = track.find('span', {'class': 'trackYear'}).getText().strip(' ()')
            artist = track.find_all('span', {'class': 'trackArtistName'})

            trackinfo = self.process_artists(artist)

            info = {
                'Title': title,
                'Year': year,
                'Artist': trackinfo['Artist'],
                'Producer': trackinfo['Producer'],
                'Features': trackinfo['Features'],  # TODO
                'SampledIn': None,  # TODO
                'Sampled': None  # TODO
            }

            print(info)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrapesongs_file(1)
