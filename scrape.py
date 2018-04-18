from dbinteract import DillaDB
from webscrape import Scraper


def scrape(numfiles):
    scraper = Scraper()
    db = DillaDB()
    print("scraping {} files".format(numfiles))
    for pagenum in range(1, numfiles+1):
        songsinfo = scraper.scrapesongs_file(pagenum)
        for song in songsinfo:
            db.addinfo(song)
        print("Finished a page!")


if __name__ == "__main__":
    scrape(20)


