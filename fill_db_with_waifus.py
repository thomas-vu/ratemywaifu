from sys import stdin
from app import db
from app.models import Waifu, WaifuTags, WaifuAverages, Anime

A = [line.split('$') for line in stdin]

for i, character in enumerate(A):
    waifu = Waifu(name        = character[1],
                  description = character[5],
                  image       = character[2],
                  url         = character[0],
                  anime_name  = Anime.query.filter_by(name=character[3]).first_or_404().name,
                  anime_id    = Anime.query.filter_by(name=character[3]).first_or_404().id)
    #print(waifu)
    db.session.add(waifu)
    B = character[4].split(',')
    for ts in B:
        tags = WaifuTags(waifu_name = character[1], tag = ts)
        db.session.add(tags)

    averages = WaifuAverages(waifu_id = str(i+1),
                             appearance_total='0',
                             personality_total='0',
                             strength_total='0',
                             intelligence_total='0',
                             num_ratings='0')
    db.session.add(averages)

db.session.commit()
