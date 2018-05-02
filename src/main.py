from src import webscraping as ws
import src.gui.mainWindow as mw
from src.data import createDB

def main():
    # Create db
    createDB.dataconnect()

    # Draw main window
    mw.IMDBGUI().drawMainWindow()


main()

# Close the db connection!
ws.db.close()

