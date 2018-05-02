import matplotlib . pyplot as plt
from src.data import getData
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def plotActorGenre(frame_to_add_to, actorID):
    # Get top 5 of the actorgenres.
    actorGenres = getData.getActorGenres(actorID)
    sizes = []
    labels = []

    for eachActorGenre in actorGenres:
        sizes.append(eachActorGenre[0])
        labels.append(eachActorGenre[1])

    colors = "bgrcmykw"

    explode = []
    for i in actorGenres:  explode.append(0)
    explode[0] = 0.1 # only "explode" the 1st slice

    # Create figure as container for the plot
    f = Figure(figsize=(6.5, 5), dpi=100, facecolor='white')
    a = f.add_subplot(1, 1, 1)

    # Plot the pie to the container
    a.pie(sizes,
            explode=explode,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            shadow=True,
            startangle=90)

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    a.axis('equal')

    # Create canvas
    canvas = FigureCanvasTkAgg(f, master=frame_to_add_to).get_tk_widget()

    return canvas




