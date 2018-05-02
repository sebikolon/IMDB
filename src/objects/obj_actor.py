import sqlite3
from src.objects import obj_actor

class Actor:
   def __init__(self, actorID, surname, prename, date_of_birth, origin, photo_link, description):
      self.actorID = actorID
      self.surname = surname
      self.prename = prename
      self.date_of_birth = date_of_birth
      self.origin = origin
      self.photo_link = photo_link
      self.description = description



