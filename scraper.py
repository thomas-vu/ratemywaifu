from sys import stdin
from app import db
from app.models import Waifu

A = [line.split('$') for line in stdin]

for character in A:
    waifu = Waifu(name        = character[1],
                  description = character[5],
                  image       = character[2],
                  url         = character[0],
                  anime_name  = character[3])
    #print(waifu)
    db.session.add(waifu)

db.session.commit()
