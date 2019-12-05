from sys import stdin
from app import db
from app.models import Anime

A = [line.split('$') for line in stdin]

for show in A:
    anime = Anime(name         = show[1],
                  season       = show[3],
                  year         = show[4],
                  num_episodes = show[5],
                  esrb         = show[6],
                  description  = show[9],
                  image        = show[2],
                  url          = show[0])
    #print(anime)
    db.session.add(anime)

db.session.commit()
