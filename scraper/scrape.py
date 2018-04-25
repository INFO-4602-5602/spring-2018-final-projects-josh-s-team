from dbinteract import DillaDB
from webscrape import Scraper


def scrape(numfiles):
    scraper = Scraper()
    db = DillaDB()
    print("scraping {} files".format(numfiles))
    for pagenum in range(1, numfiles+1):
        print("Scraping page# " + str(pagenum))
        songsinfo = scraper.scrapesongs_file(pagenum)
        for song in songsinfo:
            db.addinfo(song)
        print("Finished a page!")


def scrapepage(pagenum):
    scraper = Scraper()
    db = DillaDB()
    print("Scraping page# {}".format(pagenum))
    songsinfo = scraper.scrapesongs_file(pagenum)
    for song in songsinfo:
        db.addinfo(song)


if __name__ == "__main__":
    scrape(72)
    # scrapepage(15)
