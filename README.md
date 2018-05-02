# IMDB
Overview over the top 50 actors and actresses of the [Image Movie Database](http://www.imdb.com/list/ls053501318/), scraped with Python.

**This  software provides the following functionality:**
1. List of all available actors and actresses
2. About the actor/actresses
3. All time movie names and years
4. Awards to actor/actresses in different years
5. Movie genere of actor/actresses
6. Average rating of their movies (overall and each year)
7. Top 5 movies, their respective years and genre

# Dependencies#
* PyCharm Community Edition for developing purposes
* SQLiteBrowser (http://sqlitebrowser.org/) to view the database file which is generated from the software

# Built With #
* BeautifulSoup4 4.4.1 (for storing scraped web pages)
* lxml 3.6 (for parsing DOM elements)
* sqlite3 (for establishing a database connection)
* matplotlib 1.5.1 (for plotting the pie chart)
* pip 8.1.2 (for installing modules in the IDE)
* requests 2.10.0 (for accessing web pages)
* From Python: re, datetime, tkinter (presenting the GUI)

For using *lxml*, the following commands in the windows console are necessary:

##### Configure Python to support wheel files:

```
#!python

python.exe -m pip install wheel
```

##### Install the following .whl file ([Link](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml”)):

```
#!python

python.exe -m pip install lxml-3.6.0-cp35-cp35m-win32.whl
```

# How to use (Get started):#
The software creates a database file on startup. This file contains all the scraped data and is stored in the root directory.

When a database file already exists, the GUI opens and displays all actors instantly.
When no file exists, the user has the option to scrap the data from the internet.

To show the functionality without delay and waiting time, a complete database file ('Actor_database.db') is stored under folder 'src'. When the software opens, you can instantly start to try it out.
