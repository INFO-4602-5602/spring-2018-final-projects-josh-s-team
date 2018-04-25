# J Dilla / whosampled.com Webscraper
------------------------------------
#### Author: Evan James
#### Last updated: 4/22/2018
##### These are instructions on how to set up the MySQL database to hold all of the data, and to run the Python scripts included in this folder to scrape the webpages (which had to be downloaded, unfortunately) to populate the database. This will then be used to export as a CSV / JSON file to be used in the rendering of our visualization.

  
### Instructions: 
- Download and install your favorite MySQL client
  - [Windows](https://dev.mysql.com/downloads/installer/) - This link is to the dev.mysql page to download the Windows installer.
  - [MacOS](https://dev.mysql.com/doc/mysql-osx-excerpt/5.7/en/osx-installation-pkg.html) - This link is to a walkthrough to install the MacOS version of MySQL. 
  - [Linux](https://dev.mysql.com/doc/refman/8.0/en/linux-installation.html) - This is a link to a list of different MySQL installation methods for various Linux systems. I recommend [MariaDB](https://mariadb.org/).
- Once your MySQL server is set up, log in as root while in the `scraper/` directory and run `source createdb.sql;`. This will create the needed database, user, permissions for that user, and create the tables. 
- After running the script, check to make sure the tables were created correctly. In the MySQL prompt, type `use dilla;`, then `show tables;`. There should be 5 tables shown: Artists, DillaSongs, Rel, Samples, and Songs
- Now run the webscraper. In the `scraper/` directory, run the command `python3 scrape.py`. This will run through each page, which are kept in the `pages/` folder, and scrape the necessary information and then add to the database. The program will print to console when a page is started and finished successfully.
- **Note:** if the `scrape.py` script fails for any reason, the database will have to be reset before it can begin to be populated again. I had to do this roughly 1,000 times, so I wrote a sql script to do this: log into your MySQL server as root while still in the `scraper/` directory and run `source rebuilddb.sql;`. This will drop the whole database and then run the database initialization script again.
- After the database is populated, check to see if the number of entries in each table is correct. Use the `SELECT * FROM Songs;` command, replacing "Songs" with "Artsits" or "Rel" as needed. If everything went well, there should be:
  - Songs: 1746 rows
  - Artists: 631 rows
  - Rel: 1025 rows
- The other two tables (well, they're views, but essentially tables) are DillaSongs and Samples, which are there just for ease of looking up songs that are strictly by J Dilla and those which are just samples.
- Next, we just have to figure out how to export all the appropriate data as a CSV / JSON. That's to come.
