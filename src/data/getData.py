import sqlite3
from src.objects import obj_actor
from src.objects import obj_film
from src.objects import obj_award
from src import webscraping
from datetime import datetime

def getActor(actorID):
    db = sqlite3.connect(webscraping.path_to_database)
    myActor = None

    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM actor WHERE ActorID=?''', (actorID,))

    # retrieve all rows
    result_Actor = cursor.fetchall()
    if result_Actor:
        fetchAll_myActor = result_Actor  # get latest FilmID
    else:
        fetchAll_myActor = None

    if fetchAll_myActor:
        for row in fetchAll_myActor:
            # Create new Actor object
            myActor = obj_actor.Actor(row[0],
                                      row[1],
                                      row[2],
                                      datetime.strptime(row[3], '%Y-%m-%d'),
                                      row[4],
                                      row[5],
                                      row[6],
            )

    db.close()
    return myActor

def getAllActors():
    db = sqlite3.connect(webscraping.path_to_database)
    myActorList = []

    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM actor''')

    # retrieve all rows
    result_AllActors = cursor.fetchall()
    if result_AllActors:
        fetchAllActors = result_AllActors  # get latest FilmID
    else:
        fetchAllActors = None

    if fetchAllActors:
        actor_counter = 0
        for row in fetchAllActors:
            # Create new Actor object
            myActor = obj_actor.Actor(row[0],
                                      row[1],
                                      row[2],
                                      datetime.strptime(row[3], '%Y-%m-%d'),
                                      row[4],
                                      row[5],
                                      row[6],
            )
            myActorList.append(myActor)
            actor_counter += 1

    db.close()
    return myActorList

def getActorGenres(actorID):
    db = sqlite3.connect(webscraping.path_to_database)
    myActorGenreList = []

    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''select Anzahl, Description from
                    (select count (*) as Anzahl, Description
                    from filmgenres fg
                    INNER JOIN genre g on g.GenreID = fg.GenreID
                    where fg.FilmID IN( select filmID from film where actorid = ?)
                    group by description
                    order by anzahl desc) LIMIT 5''', (actorID,))

    # retrieve all rows
    actorgenres = cursor.fetchall()
    if actorgenres:
        fetchAllActorGenres = actorgenres
    else:
        fetchAllActorGenres = None

    if fetchAllActorGenres:
        for actorgenre in fetchAllActorGenres:
            myActorGenreList.append(actorgenre)

    db.close()
    return myActorGenreList

def getFilm(FilmID):
    db = sqlite3.connect(webscraping.path_to_database)
    myFilm = None

    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM film WHERE FilmID = ?''', (FilmID,))

    # retrieve all rows
    result_allFilms = cursor.fetchall()
    if result_allFilms:
        fetchAll_myFilm = result_allFilms  # get latest FilmID
    else:
        fetchAll_myFilm = None

    if fetchAll_myFilm:
        for thisFilm in fetchAll_myFilm:

            # Select all genres for this film
            cursor.execute('''SELECT distinct g.Description FROM filmgenres fg
                              INNER JOIN genre g
                              ON g.genreID= fg.GenreID
                              WHERE fg.FilmID = ?''', (thisFilm[0],))
            myFilmGenres = cursor.fetchall()
            if not myFilmGenres:
                myFilmGenres = [0]

            # Create new Film object
            myFilm = obj_film.Film(filmID = thisFilm[0],
                                   actorID = thisFilm[1],
                                   title= thisFilm[2],
                                   year= thisFilm[3],
                                   genres= myFilmGenres,
                                   rating= thisFilm[5], )

    db.close()
    return myFilm

def getAllFilmsOfActor(ActorID):
    db = sqlite3.connect(webscraping.path_to_database)
    myFilmList = []

    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM film WHERE ActorID = ?''',(ActorID,))

    # retrieve all rows
    result_AllFilmsOfActor = cursor.fetchall()
    if result_AllFilmsOfActor:
        fetchAllFilms = result_AllFilmsOfActor  # get latest FilmID
    else:
        fetchAllFilms = None

    if fetchAllFilms:
        films_counter = 0
        for row in fetchAllFilms:

            # Select all genres for this film
            cursor.execute('''SELECT DISTINCT g.Description FROM filmgenres fg
                              INNER JOIN genre g
                              ON g.genreID= fg.GenreID
                              WHERE fg.FilmID = ?''', (row[0],))
            result_FilmOfActor = cursor.fetchall()
            if result_FilmOfActor:
                myFilmGenres = result_FilmOfActor
            else:
                myFilmGenres = [0]

            # Create new Film object
            myFilm = obj_film.Film(filmID = row[0],
                                   actorID = row[1],
                                   title= row[2],
                                   year= row[3],
                                   genres= myFilmGenres,
                                   rating= row[4], )
            myFilmList.append(myFilm)
            films_counter += 1

    db.close()
    return myFilmList

def getTop5FilmsOfActor(ActorID):
    db = sqlite3.connect(webscraping.path_to_database)
    myTop5FilmList = []

    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM film WHERE ActorID = ? ORDER BY rating DESC LIMIT 5''',(ActorID,))

    # retrieve all rows
    result_Top5FilmsOfActor = cursor.fetchall()
    if result_Top5FilmsOfActor:
        fetchtop5Films = result_Top5FilmsOfActor  # get latest FilmID
    else:
        fetchtop5Films = None

    if fetchtop5Films:
        films_counter = 0
        for row in fetchtop5Films:

            # Select all genres for this film
            cursor.execute('''SELECT DISTINCT g.Description FROM filmgenres fg
                              INNER JOIN genre g
                              ON g.genreID= fg.GenreID
                              WHERE fg.FilmID = ?''', (row[0],))
            result_Top5FilmsOfActor = cursor.fetchall()
            if result_Top5FilmsOfActor:
                myFilmGenres = result_Top5FilmsOfActor
            else:
                myFilmGenres = [0]

            # Create new Film object
            myFilm = obj_film.Film(filmID = row[0],
                                   actorID = row[1],
                                   title= row[2],
                                   year= row[3],
                                   genres= myFilmGenres,
                                   rating= row[4], )
            myTop5FilmList.append(myFilm)
            films_counter += 1

    db.close()
    return myTop5FilmList

def getAllYearsOfAwardsOfActor(ActorID):
    db = sqlite3.connect(webscraping.path_to_database)
    myYearList = []

    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT DISTINCT year FROM award WHERE ActorID = ? ORDER BY YEAR DESC ''',(ActorID,))

    # retrieve all rows
    result_AllYearsOfAwardsOfActor = cursor.fetchall()
    if result_AllYearsOfAwardsOfActor:
        fetchAllYears = result_AllYearsOfAwardsOfActor
    else:
        fetchAllYears = None

    if fetchAllYears:
        for year in fetchAllYears:
            myYearList.append(year)

    db.close()
    return myYearList

def getAllAwardsOfYearOfActor(ActorID, Year):
    db = sqlite3.connect(webscraping.path_to_database)
    myAwardList = []

    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM award WHERE ActorID = ? AND Year = ?''',(ActorID,Year,))

    # retrieve all rows
    result = cursor.fetchall()
    if result:
        fetchAllAwards = result
    else:
        fetchAllAwards = None

    if fetchAllAwards:
        for award in fetchAllAwards:
            # Create new Award object
            myAward = obj_award.Award(awardID= award[0],
                                      description=award[1],
                                      name=award[2],
                                      year=award[3],
                                      actorID=award[4])
            myAwardList.append(myAward)

    db.close()
    return myAwardList



def getRating(actorID, ofYear):
    db = sqlite3.connect(webscraping.path_to_database)

    # Get a cursor object
    cursor = db.cursor()

    #if actorID == 0: actorID

    if ofYear == 0: cursor.execute('''SELECT rating FROM film WHERE actorID=?''', (actorID,))      # overall years
    else: cursor.execute('''SELECT rating FROM film WHERE actorID=? AND year=?''', (actorID, ofYear,))    # over a specific year

    # Retrieve all rows
    result = cursor.fetchall()
    if result:
        fetchAll_Ratings = result
    else:
        fetchAll_Ratings = None

    # Sum up the ratings
    ratingAverage = 0
    numberOfRatings = 0
    if fetchAll_Ratings:
        for eachRating in fetchAll_Ratings:
            ratingAverage = ratingAverage + eachRating[0]
            numberOfRatings = numberOfRatings + 1

    db.close()

    if numberOfRatings == 0:
        return 0
    else:
        return round(ratingAverage / numberOfRatings, 1)