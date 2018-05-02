from tkinter import ttk
from tkinter import *
import tkinter as tk
import src.data.getData as getData
import src.data.createDB as createDB
import src.data.deleteData as deleteData
from src.gui import plot
from tkinter import messagebox
from src import webscraping

# create main window
tkTop = tk.Tk()

class IMDBGUI:

    def sort_List(self, tree_Actors, col, reverse):
        if col=='#':
            l = [(tree_Actors.set(k, col), k) for k in tree_Actors.get_children('')]
            # Convert the actor number from string to int
            l = [[int(x[0]), x[1]] for x in l]
            l.sort(reverse=reverse)
        else:
            l = [(tree_Actors.set(k, col), k) for k in tree_Actors.get_children('')]
            l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tree_Actors.move(k, '', index)

            # reverse sort next time
            tree_Actors.heading(col, command=lambda _col=col: self.sort_List(tree_Actors, col, not reverse))

    def OnSingleClick(self, event, right_frame, tree):
        # Identify the region of the click event to make sure that no heading is clicked
        region = tree.identify("region", event.x, event.y)
        if region != "heading":
            # Get the currently selected actor
            item = tree.identify('item', event.x, event.y)
            myActorID = tree.item(item, "text")

            # Make sure that the item is not a root item
            if item != 'root1' and item != 'root2' and item != 'root3' and item != 'root4' and item != 'root5':
                # Delete all children from target frame
                for child in right_frame.winfo_children():
                    child.destroy()

                # Create a new right frame
                self.createRightColumn(right_frame, myActorID)
            else: # If the item IS a root item
                # collapse all other root items
                if item == 'root1':
                    if tree.exists('root2'): tree.item('root2', open=FALSE)
                    if tree.exists('root3'): tree.item('root3', open=FALSE)
                    if tree.exists('root4'): tree.item('root4', open=FALSE)
                    if tree.exists('root5'): tree.item('root5', open=FALSE)
                elif item == 'root2':
                    if tree.exists('root1'): tree.item('root1', open=FALSE)
                    if tree.exists('root3'): tree.item('root3', open=FALSE)
                    if tree.exists('root4'): tree.item('root4', open=FALSE)
                    if tree.exists('root5'): tree.item('root5', open=FALSE)
                elif item == 'root3':
                    if tree.exists('root1'): tree.item('root1', open=FALSE)
                    if tree.exists('root2'): tree.item('root2', open=FALSE)
                    if tree.exists('root4'): tree.item('root4', open=FALSE)
                    if tree.exists('root5'): tree.item('root5', open=FALSE)
                elif item == 'root4':
                    if tree.exists('root1'): tree.item('root1', open=FALSE)
                    if tree.exists('root2'): tree.item('root2', open=FALSE)
                    if tree.exists('root3'): tree.item('root3', open=FALSE)
                    if tree.exists('root5'): tree.item('root5', open=FALSE)
                elif item == 'root5':
                    if tree.exists('root1'): tree.item('root1', open=FALSE)
                    if tree.exists('root2'): tree.item('root2', open=FALSE)
                    if tree.exists('root3'): tree.item('root3', open=FALSE)
                    if tree.exists('root4'): tree.item('root4', open=FALSE)


    def createLeftColumn(self, right_frame, canv_left):
        # Define the columns
        columns = ("PRENAME", "SURNAME")

        # Create the TREEVIEW
        tree_Actors = ttk.Treeview(canv_left, columns=columns, height=50)

        # Define column width
        tree_Actors.column("#0", minwidth=0, width="70", stretch=YES) # First column
        tree_Actors.column("PRENAME", width=90)
        tree_Actors.column("SURNAME", width=90)

        # Define headings and prepare the sorting
        for col in columns:
            tree_Actors.heading(col,
                                text=col)
                                #,command=lambda _col=col: self.sort_List(tree_Actors, _col, False))

        # Hide first column with actorID
        #tree_Actors["show"]="headings"

        # Get all actors from database
        allActors = getData.getAllActors()
        len_allActors = len(allActors)

        # Insert root items
        if len_allActors > 0 :
            tree_Actors.insert("", 'end', "root1", text="Top 10", open=TRUE)
        if len_allActors > 10 :
            tree_Actors.insert("", 'end', "root2", text="11 - 20" )
        if len_allActors > 20 :
            tree_Actors.insert("", 'end', "root3", text="21 - 30" )
        if len_allActors > 30 :
            tree_Actors.insert("", 'end', "root4", text="31 - 40" )
        if len_allActors > 40 :
            tree_Actors.insert("", 'end', "root5", text="41 - 50" )

        eachActorCounter = 0
        for eachActor in allActors:
            eachActorCounter += 1
            rootID = ""
            if eachActorCounter <=10:                                 rootID =  "root1"
            elif eachActorCounter > 10 and eachActorCounter <=20:     rootID =  "root2"
            elif eachActorCounter > 20 and eachActorCounter <=30:     rootID =  "root3"
            elif eachActorCounter > 30 and eachActorCounter <= 40:    rootID =  "root4"
            elif eachActorCounter > 40 :                              rootID =  "root5"

            # Insert under root, at the end, leading column, values
            tree_Actors.insert(rootID, 'end',
                               text = getattr(eachActor,'actorID') ,
                               values=(getattr(eachActor, 'prename'),
                                       getattr(eachActor, 'surname'))
                               )
            # Bind single click action to list item
            tree_Actors.bind("<Button-1>", lambda event : self.OnSingleClick(event, right_frame, tree_Actors))

        # Bind tree view to frame
        canv_left.create_window(0, 0, anchor=NW, window=tree_Actors)

    def fillAllFilmsAndRatings(self, notebook, myActor):
        frame_films_ratings = ttk.Frame(notebook)

        # Get myActorID
        if not myActor:
            myActorID = 0
        else:
            myActorID = getattr(myActor,'actorID')

        # Create a label
        lbl_allFilmsAndRatings_sort = Label(frame_films_ratings,
                                            text="You can sort the columns by clicking on the heading!\n",
                                            font = ('Verdana', 8, 'bold'))
        lbl_allFilmsAndRatings_sort.grid(row=1, column=1, sticky=NSEW)

        # Define the columns
        columns = ("TITLE", "YEAR", "GENRE", "RATING")

        # Create the TREEVIEW
        tree_Films_of_Actor = ttk.Treeview(frame_films_ratings, columns=columns, height=23)

        # Define column width
        tree_Films_of_Actor.column("TITLE", minwidth=200)
        tree_Films_of_Actor.column("YEAR", minwidth=40, width=40)
        tree_Films_of_Actor.column("GENRE", minwidth=180)
        tree_Films_of_Actor.column("RATING", minwidth=20)

        # Define headings and prepare the sorting
        for col in columns:
            tree_Films_of_Actor.heading(col,
                                text=col,
                                command=lambda _col=col: self.sort_List(tree_Films_of_Actor, _col, False))

        # Hide first column with title
        tree_Films_of_Actor["show"] = "headings"

        # Get all films of actor
        all_Films_of_Actor = getData.getAllFilmsOfActor(myActorID)

        for eachFilm in all_Films_of_Actor:
            # Get film genres
            all_Genres_of_Film = getattr(eachFilm, 'genres')
            myFilmGenres = ""
            genrecounter = 0
            len_myFilmGenres = len(all_Genres_of_Film)
            if all_Genres_of_Film:
                for eachGenre in all_Genres_of_Film:
                    if eachGenre:
                        myFilmGenres = myFilmGenres  + str(eachGenre[0])
                        if genrecounter < len_myFilmGenres -1:
                            myFilmGenres = myFilmGenres + ", "
                        genrecounter += 1

            # Insert under root, at the end, etc
            tree_Films_of_Actor.insert("", 'end',  text=getattr(eachFilm, 'filmID'),
                               values=(getattr(eachFilm, 'title'),
                                       getattr(eachFilm, 'year'),
                                       myFilmGenres,
                                       getattr(eachFilm, 'rating')))

            # Bind single click action to list item
            #all_Films_of_Actor.bind("<Button-1>", lambda event: self.OnSingleClick(event, tkTop, all_Films_of_Actor))

        # Bind tree view to frame
        tree_Films_of_Actor.grid(row=2, column=1, sticky=W)

        return frame_films_ratings

    def fillAbout(self, notebook, myActor):
        frame_about = ttk.Frame(notebook)

        # Get myActorID
        if not myActor:
            myActorID = 0
        else:
            myActorID = getattr(myActor, 'actorID')

        # Fill table
        # Name
        lbl_name = Label(frame_about, text=getattr(myActor, 'prename') + " " + getattr(myActor, 'surname'), font=('Verdana', 8, 'bold'))
        lbl_name.grid(row=1, column=1, sticky=W)

        # Date of birth and origin
        lbl_date_origin = Label(frame_about,
              text="was born on " + getattr(myActor, 'date_of_birth').strftime("%B %d, %Y")
                   + " in "
                   + getattr(myActor, 'origin') + ".")
        lbl_date_origin.grid(row=2, column=1, sticky=W)


        # Average rating heading
        lbl_actorgenre_heading =  Label(frame_about,
                                       text="\nAverage rating of " + getattr(myActor, 'prename') + " " + getattr(myActor, 'surname') + "'s movies:\n",
                                       font=('Verdana', 8, 'bold'))
        lbl_actorgenre_heading.grid(row=3, column=1, sticky=W)


        # Average ratings over all years - Label
        lbl_average_rating_overall_Years = Label(frame_about,
                           text="The average rating over all years is: " + str(getData.getRating(myActorID,0)),
                           font=('Verdana', 8))
        lbl_average_rating_overall_Years.grid(row=4, column=1, sticky=W)


        # Average ratings of each year - Label
        lbl_scale_textvar = StringVar()
        lbl_average_rating_each_year = Label(frame_about,
                                   textvariable=lbl_scale_textvar,
                                   font=('Verdana', 8))
        lbl_average_rating_each_year.grid(row=5, column=1, sticky=W)


        # Average ratings - Scale
        scl_from_all = getData.getAllFilmsOfActor(myActorID)
        if scl_from_all:
            scl_from = int(getattr(scl_from_all[len(scl_from_all)-1], 'year'))

            # Find first film with a valid year
            count = 0
            while (getattr(scl_from_all[count], 'year') == ""):
                count += 1
            scl_to = int(getattr(scl_from_all[count], 'year'))
        else:
            scl_from = 0
            scl_to = 0

        scl_average_rating =  Scale(frame_about,
                                    from_=scl_from,
                                    to=scl_to,
                                    length=500,
                                    orient=HORIZONTAL,
                                    command=
                                    lambda temp=0.0:updateDepositLabel(str(getData.getRating(myActorID, scl_average_rating.get())))
                                    )
        scl_average_rating.grid(row=6, column=1, sticky=W)

        #Updates the label text of average rating
        def updateDepositLabel(rating_of_year):
            if rating_of_year == "0" or rating_of_year == "0.0":
                lbl_scale_textvar.set("In this year there is no rating to display.")
            else:
                lbl_scale_textvar.set("Average rating of the selected year is: " + rating_of_year)

        #btn_actorgenre = tk.Button(frame_about,
        #text = "Take a closer look at his genres",
        #command = lambda tabid = 3: notebook.select(tabid))
        #btn_actorgenre.grid(row=4, column=1, sticky=W)



        # Biography heading
        lbl_description_heading = Label(frame_about,
                                        text="\nShort biography:",
                                        font=('Verdana', 8, 'bold'))
        lbl_description_heading.grid(row=7, column=1, sticky=W)

        # Prepare the biography shortening
        myBiography_original = getattr(myActor,'description')
        myBiography_shorten = myBiography_original[0:1200] + "..." # Cut the biography to 1200 chars
        myBiography = myBiography_original

        # Short the biography
        if len(myBiography_original) > len(myBiography_shorten):
            myBiography =  myBiography_shorten

            # Biography button, if bio is too long
            tkButton_NewWindow_biography = tk.Button(
                frame_about,
                text="Show full short biography",
                command=lambda: self.create_window_biography(myBiography_original))
            tkButton_NewWindow_biography.grid(row=9, column=1, sticky=NW)


        # Biography label
        lbl_description = Label(frame_about,
                                text=myBiography,
                                width=80,
                                fg='black',
                                wraplength=520,
                                anchor=NW,
                                justify=LEFT,
                                pady=10)
        lbl_description.grid(row=8, column=1, sticky=W)

        return frame_about

    def create_window_biography(self, myText):
        wndw_biography = tk.Toplevel(tkTop)
        wndw_biography.geometry("1200x1200")

        lbl_wndw_biography_header = Label(wndw_biography,
                                   text="Enjoy to read the biography here:",
                                   anchor=NW,
                                   pady=10,
                                   font=('Verdana', 8, 'bold')
                                   )
        lbl_wndw_biography_header.grid(row=1, column=1, sticky=NW)

        lbl_wndw_biography = Label(wndw_biography,
                                   text=myText,
                                   wraplength=1200,
                                   anchor=NW,
                                   justify=LEFT,
                                   pady=10
                                   )
        lbl_wndw_biography.grid(row=2, column=1, sticky=NW)

    def fillAwards(self, notebook, myActor):
        frame_awards = ttk.Frame(notebook)

        # Get myActorID
        if not myActor:
            myActorID = 0
        else:
            myActorID = getattr(myActor, 'actorID')

        # Define the columns
        columns = ("NAME", "DESCRIPTION")

        # Create the TREEVIEW
        tree_Awards_of_Actor = ttk.Treeview(frame_awards, columns=columns, height=25, selectmode=BROWSE)

        # Define column width
        tree_Awards_of_Actor.column("NAME",  width=250,  stretch=YES)
        tree_Awards_of_Actor.column("DESCRIPTION", width=300, stretch=YES)
        tree_Awards_of_Actor.column("#0", minwidth=0, width="70", stretch=YES) # First column

        # Define headings and prepare the sorting
        for col in columns:
            tree_Awards_of_Actor.heading(col,
                                        text=col)
                                        #,command=lambda _col=col: self.sort_List(tree_Awards_of_Actor, _col, False))

        # Hide first column with title
        #tree_Awards_of_Actor["show"] = "headings"


        # Get all years of awards
        all_Years = getData.getAllYearsOfAwardsOfActor(myActorID)

        for eachYear in all_Years:
            # insert new line
            tree_Awards_of_Actor.insert("", 'end', "Year_" + str(eachYear[0]), text=str(eachYear[0]), open=TRUE)

            # Get all films of actor
            all_Awards_Of_Year_Of_Actor = getData.getAllAwardsOfYearOfActor(myActorID, int(eachYear[0]))

            for eachAward in all_Awards_Of_Year_Of_Actor:
                # Insert new sub item
                tree_Awards_of_Actor.insert("Year_" + str(eachYear[0]), 'end', text='',
                                       values=(getattr(eachAward, 'name'),
                                               str(getattr(eachAward, 'description'))
                                               ))

            # Bind single click action to list item
            # all_Films_of_Actor.bind("<Button-1>", lambda event: self.OnSingleClick(event, tkTop, all_Films_of_Actor))


        # Bind tree view to frame
        tree_Awards_of_Actor.grid(row=3, column=1, columnspan=2, sticky=W)

        return frame_awards

    def fillActorGenres(self, notebook, myActor):
        frame_actorGenres = ttk.Frame(notebook)

        # Get myActorID
        if not myActor:
            myActorID = 0
        else:
            myActorID = getattr(myActor, 'actorID')

        # Add a label
        lbl_actorGenre = Label(frame_actorGenres,
                              text="Here you can see the distribution of the TOP 5 genres of "
                                   + getattr(myActor,'prename') + " "
                                   + getattr(myActor,'surname') + "!\n",
                              font=('Verdana', 8, 'bold'))
        lbl_actorGenre.grid(row=1, column=1, sticky=W)


        # Add a pie plot
        myPlot = plot.plotActorGenre(frame_actorGenres, myActorID)
        myPlot.grid(row=2, column=1, sticky=W)

        return frame_actorGenres

    def fillTop5Films(self, notebook, myActor):
        frame_top5Movies = ttk.Frame(notebook)

        # Get myActorID
        if not myActor:
            myActorID = 0
        else:
            myActorID = getattr(myActor, 'actorID')

        # Add a label - heading
        lbl_top5Films_heading = Label(frame_top5Movies,
                               text="Here are the TOP 5 movies of "
                                    + getattr(myActor, 'prename') + " "
                                    + getattr(myActor, 'surname') + "!\n",
                               font=('Verdana', 8, 'bold'))
        lbl_top5Films_heading.grid(row=1, column=1, columnspan=4, sticky=W)

        # Get Top5 Films from database
        top5films = getData.getTop5FilmsOfActor(myActorID)

        def gettop5FilmGenres(eachFilm):
            # Get the genres for the Top5 Films
            myFilmGenres = ""
            all_Genres_of_this_Film = getattr(eachFilm, 'genres')
            genrecounter = 0
            len_myFilmGenres = len(all_Genres_of_this_Film)
            if all_Genres_of_this_Film:
                for eachGenre in all_Genres_of_this_Film:
                    if eachGenre:
                        myFilmGenres = myFilmGenres + str(eachGenre[0])
                        if genrecounter < len_myFilmGenres - 1:
                            myFilmGenres = myFilmGenres + ", "
                        genrecounter += 1
            if myFilmGenres =="": myFilmGenres = "No Genre."
            return myFilmGenres


        rowcounter = 2
        # Add labels and rank image for each Film
        for film in top5films:
            # Add a label - RANK
            lbl_top5Films_RANK = Label(frame_top5Movies,
                                       text=rowcounter-1,
                                       font=('Bodoni MT Black', 25, 'bold'))
            lbl_top5Films_RANK.grid(row=rowcounter, column=1, sticky=W)


            # Add a label - TITLE
            lbl_top5Films_TITLE = Label(frame_top5Movies,
                                        text="" + getattr(film, 'title') + " (" +  str(getattr(film, 'year')) + ") \n",
                                        font=('Verdana', 10))
            lbl_top5Films_TITLE.grid(row=rowcounter, column=2, sticky=W)


            # Add a label - RATING
            lbl_top5Films_RATING = Label(frame_top5Movies,
                                          text="Rating: " + str(getattr(film, 'rating')) + "\n",
                                          font=('Verdana', 10, 'bold'))
            lbl_top5Films_RATING.grid(row=rowcounter, column=3, sticky=NW)


            # Add a label - GENRES
            lbl_top5Films_GENRES = Label(frame_top5Movies,
                                         text=" -  " + gettop5FilmGenres(film) + "\n",
                                         font=('Verdana', 10))
            lbl_top5Films_GENRES.grid(row=rowcounter, column=4, sticky=NW)

            rowcounter += 1



        return frame_top5Movies

    def createRightColumn(self, right_frame, myActorID):
        myActor = getData.getActor(myActorID)
        # Initiate notebook layout
        notebook = ttk.Notebook(right_frame)

        # Add grid
        notebook.grid(row=3, column=2, columnspan=5, sticky='N')

        # Add frames
        notebook.add(self.fillAbout(notebook, myActor),              text='About the actor', padding=4)
        notebook.add(self.fillAllFilmsAndRatings(notebook, myActor), text='Films and ratings', padding=4)
        notebook.add(self.fillAwards(notebook, myActor),             text='Awards to actor', padding=4)
        notebook.add(self.fillActorGenres(notebook,myActor),         text='Actor Genres', padding=4)
        notebook.add(self.fillTop5Films(notebook, myActor),          text='Top 5 movies', padding=4)


    def drawMainWindow(self):
        tkTop.resizable(width=False, height=False)
        tkTop.geometry('900x600')
        tkTop.title("Image Movie Database - OTH Regensburg")

        # Add image
        img_imdb = tk.PhotoImage(file="../img/IMDb_logo.png")
        lbl_img_imdb = Label(tkTop, image=img_imdb)
        lbl_img_imdb.grid(row=1, column=1)

        # Add welcome text
        tkLabelTop = tk.Label(tkTop,
                              text=" These are the top 50 Hollywood actors and actresses. \n",
                              font=('Verdana', 9, 'bold'))
        tkLabelTop.grid(row=1, column=2)


        # Function for the scrap button
        def scrapNow():
            if messagebox.askokcancel("Information", "When you press OK, the top 50 actors will be scrapped from the IMDB Homepage. \n"
                                                     "This will take about 60 Minutes.\n "
                                                     "All data which was scrapped before will be deleted.\n"
                                                     "Do you want to scrap now?"):

                deleteData.deleteData()
                createDB.dataconnect()
                webscraping.getMainList()
                self.drawMainWindow()

        # Add Scrap button
        btn_ScrapData = tk.Button(
                        tkTop,
                        text = "Scrap Now!",
                        command=scrapNow)
        btn_ScrapData.grid(row=1, column=1, sticky=E)


        # Create frame for right column
        right_frame = Frame(tkTop)

        right_frame.grid(row=3, column=2, sticky=NW)

        if not getData.getAllActors():
            lbl_noActorSelected = Label(right_frame,
                                        text="Please srap the data first!"
                                             + "\n",
                                        font=('Verdana', 8, 'bold'))
            lbl_noActorSelected.grid(row=1, column=1, columnspan=5, padx=200, pady=200, sticky=NSEW)

        else:
            lbl_noActorSelected = Label(right_frame,
                                        text="Please select an actor first"
                                             + ".\n",
                                        font=('Verdana', 8, 'bold'))
            lbl_noActorSelected.grid(row=1, column=1, columnspan=5, padx=200, pady=200, sticky=NSEW)


        # Create frame as container for the left canvas
        left_frame = Frame(tkTop, bd=3)
        left_frame.grid(row=3, column=1, sticky=N)

        # Create canvas for left column and Add scrollbar
        canv_left = Canvas(left_frame, width=250, height=1000)
        canv_left.grid(row=3, column=1)

        # Create left column
        self.createLeftColumn(right_frame, canv_left)

        # Start the GUI
        tk.mainloop()
