import requests as rq
from bs4 import BeautifulSoup, SoupStrainer
import re
import datetime
from src.data import saveData
import sqlite3

path_to_database = 'Actor_database.db'
db = sqlite3.connect(path_to_database) # Creates or opens a file called Actor_database with a SQLite3 DB
cursor = db.cursor() # Get a cursor object

baseURL = "http://www.imdb.com"
mainListURL = "/list/ls053501318/"
biographyURL = "bio"
awardsURL = "awards"

months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

### CALL THE MAIN LIST ###
def getMainList():
    rqMainList = rq.get(baseURL + mainListURL)  # request the website
    soup = BeautifulSoup(rqMainList.text, 'lxml')

    # Get list with all actors
    allActors = soup.find('div', {'class': "list detail"})
    # Get div with all images
    allActors_images = allActors.findAll('div', {'class': 'image'})

    #tempcounter = 0
    for eachActorImage in allActors_images:
        # Get all 'a' links starting with '/name/'
        myActorImageLink_Container = eachActorImage.findAll("a", href=re.compile('^/name/'))

        for eachActorImageLink in myActorImageLink_Container:
            myActorImageLink = eachActorImageLink['href']
            if myActorImageLink:
                # STEP ONE - GET INFORMATION ABOUT ACTOR
                eachLink_photo_link = eachActorImageLink.findAll("img")
                if eachLink_photo_link[0]['src']:
                    getInformationAboutActor(myActorImageLink, eachLink_photo_link[0]['src'])

                # STEP TWO - GET ALL FILMS OF ACTOR
                getAllFilmsOfActor(myActorImageLink)

                # STEP THREE - GET ALL AWARDS OF ACTOR
                getAllAwardsOfActor(myActorImageLink)

    #print("End: ", datetime.datetime.now().time())

### GET INFORMATION ABOUT ACTOR ###
def getInformationAboutActor(link_to_actor, link_to_photo):
    rqMyInformation = rq.get(baseURL + link_to_actor + biographyURL)  # request the actor biography URL

    parse_only = SoupStrainer('div', {'class': 'article listo'})
    soupMyInformation = BeautifulSoup(rqMyInformation.text, 'lxml',parse_only=parse_only)

    myActorPrename = ""
    myActorSurname = ""
    myBiography = ""
    myOrigin = ""
    myDate_of_Birth = 0

    # Get Surname and Prename
    myActorName_Container_h3 = soupMyInformation.find('h3', attrs={"itemprop": re.compile('name')})
    if myActorName_Container_h3 != None:
        myActorName_Container = myActorName_Container_h3.findAll('a', attrs={"itemprop": re.compile('url')})
        if myActorName_Container[0] != None:
            myActorName_List = myActorName_Container[0].string.split(' ', 1)
            myActorPrename = myActorName_List[0]
            myActorSurname = myActorName_List[1]

    # Get Biography
    myBiographyContainer = soupMyInformation.find('div', {'class': 'soda odd'})
    if myBiographyContainer != None:
        myBiography_all_p = myBiographyContainer.findAll('p')
        if myBiography_all_p[0] != None:
            myBiography = removeHTMLTags(str(myBiography_all_p[0]), 'br', 'a')
            if not myBiography: myBiography="No Biography available."

    # Get origin
    myOverviewContainer = soupMyInformation.find('table', {'id': 'overviewTable'})
    if myOverviewContainer != None:
        myOverview = myOverviewContainer.findAll('a')
        if myOverview != None:
            myOrigin = str(myOverview[2].string)

            # Get date of birth
            myDate_of_Birth_DayMonth_List = myOverview[0].string.split()
            myDate_of_Birth_Day = myDate_of_Birth_DayMonth_List[0]
            myDate_of_Birth_Month = myDate_of_Birth_DayMonth_List[1]
            if myDate_of_Birth_Month in months.keys():              # parse string to int
                myDate_of_Birth_Month = months[myDate_of_Birth_Month]
                myDate_of_Birth_Year = myOverview[1].string
                myDate_of_Birth = datetime.date(int(myDate_of_Birth_Year),int(myDate_of_Birth_Month),int(myDate_of_Birth_Day))

    # Save the actor
    saveData.saveNewActor(myActorSurname, myActorPrename, myDate_of_Birth, myOrigin, link_to_photo, myBiography)

### GET ALL FILMS OF EACH ACTOR
def getAllFilmsOfActor(link_to_actor):
    rqMyActor = rq.get(baseURL + link_to_actor)  # request the actor URL
    soupMyActor = BeautifulSoup(rqMyActor.text, 'lxml')

    myActorFilms_All = soupMyActor.find('div', {'class': 'filmo-category-section'})
    myActorFilms = myActorFilms_All.findAll('div', attrs={"class": re.compile('^filmo-row')})
    myActorName = soupMyActor.find('span', attrs={"itemprop": re.compile('name')}).string

    for eachFilm in myActorFilms:
        myFilmGenre = ""
        myFilmTitle = ""
        myFilmYear = ""
        myFilmRating = 0.0

        myActorFilm_solo_title = eachFilm.findAll("a", href=re.compile('^/title/tt'))
        if myActorFilm_solo_title[0] != None:
            myFilmTitle = myActorFilm_solo_title[0].string

        myActorFilm_solo_year = eachFilm.findAll("span", {'class': "year_column"})
        if myActorFilm_solo_year[0] != None:
            myFilmYear = re.sub(re.compile('\n'), '', myActorFilm_solo_year[0].string) # remove html tags
            myFilmYear = myFilmYear.strip() # remove white spaces
            if myFilmYear != "": myFilmYear = int(myFilmYear[:4]) # only the first four characters represent a year


        ### GET FILM DETAILS - Genre and rating ####
        rqMyFilm = rq.get(baseURL + myActorFilm_solo_title[0]['href'])
        soupMyFilm = BeautifulSoup(rqMyFilm.text, 'lxml')

        #if myDiv_Subtext != None:
        if soupMyFilm:
            myGenres = soupMyFilm.findAll('span', attrs={"itemprop": re.compile('genre')})
            for eachGenre in myGenres:
                myFilmGenre = myFilmGenre + eachGenre.string + " "

        myDiv_Ratings = soupMyFilm.find('div', {'class': 'ratings_wrapper'})
        if myDiv_Ratings:
            myRatings = myDiv_Ratings.findAll('span', attrs={"itemprop": re.compile('ratingValue')})
            if myRatings:
                myFilmRating = float(myRatings[0].string)

        ### SAVE new film ###
        saveData.saveNewFilm(myActorName, myFilmTitle, myFilmYear, myFilmGenre, myFilmRating)

### GET ALL AWARDS OF EACH ACTOR
def getAllAwardsOfActor(link_to_actor):
    rqMyAwards = rq.get(baseURL + link_to_actor + awardsURL)
    soupMyAwards = BeautifulSoup(rqMyAwards.text, 'lxml')
    myAwards_All = soupMyAwards.findAll('table', {'class': 'awards'})

    myActorName = ""
    myActorName_h3 = soupMyAwards.find('h3', attrs={"itemprop": re.compile('name')})
    if myActorName_h3:
        myActorName = myActorName_h3.find('a', attrs={"itemprop": re.compile('url')}).string


    for eachTable in myAwards_All: # awards are separated by category
        tr_All = eachTable.findAll('tr') # select each award (nominated and won)
        for each_tr in tr_All:
            award_outcome_container = each_tr.find('td', {'class': 'award_outcome'})
            if award_outcome_container:
                award_outcome = award_outcome_container.find('b').string
                if award_outcome == 'Won':     # Only awards which went to the actor
                    # Get year of award
                    award_year = 0
                    award_year_container = each_tr.find('td', {'class':'award_year'})
                    if award_year_container:
                        award_year = int(award_year_container.find('a').string)

                    # Get award name
                    award_name = ""
                    award_name = str(award_outcome_container.find('span',{'class':'award_category'}).string)

                    # Get award description
                    award_description = ""
                    award_description_container = each_tr.findAll('td', {'class':'award_description'})

                    if award_description_container:
                        award_description = removeHTMLTags(str(award_description_container[0]), 'br', 'a')
                        if not award_description: award_description = "No Description available."

                    # Save new award
                    saveData.saveNewAward(award_year, award_name, award_description, myActorName)


def removeHTMLTags(html, *tags):
    soup = BeautifulSoup(html, "lxml")

    for eachtag in tags:
        if eachtag == 'br':
            for each_br in soup.findAll(eachtag):
                each_br.replaceWith('\n')
        else:
            for eachElement in soup.findAll(eachtag):
                eachElement.replaceWith(eachElement.string)

    return soup.get_text().lstrip().rstrip()

