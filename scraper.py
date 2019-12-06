from sys import stdin
from app import db
from app.models import Waifu, WaifuTags

A = [line.split('$') for line in stdin]

for character in A:
    waifu = Waifu(name        = character[1],
                  description = character[5],
                  image       = character[2],
                  url         = character[0],
                  anime_name  = character[3])
    #print(waifu)
    db.session.add(waifu)
    B = character[4].split(',')
    for ts in B:
        tags = WaifuTags(waifu_name = character[1], tag = ts)
        db.session.add(tags)

db.session.commit()
