from app import db
from app.models import User, Waifu, Rating, WaifuAverages
from random import randint

user = User(username='CatGirlLover69', email='catgirllover69@gmail.com')
user.set_password('cat')
db.session.add(user)

for _ in range(100):
    random_id = randint(1, 37)
    waifu = Waifu.query.filter_by(id=random_id).first_or_404()

    random_appearance = randint(1, 10)
    random_personality = randint(1, 10)
    random_strength = randint(1, 10)
    random_intelligence = randint(1, 10)

    rating = Rating(appearance=random_appearance, personality=random_personality, \
        strength=random_strength, intelligence=random_intelligence, wouldyou='Gladly.', \
        body='This is an example rating! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', author=user, rated=waifu)

    db.session.add(rating)

    averages = WaifuAverages.query.filter_by(id=random_id).first_or_404()
    averages.appearance_total = str(int(averages.appearance_total) + random_appearance)
    averages.personality_total = str(int(averages.personality_total) + random_personality)
    averages.strength_total = str(int(averages.strength_total) + random_strength)
    averages.intelligence_total = str(int(averages.intelligence_total) + random_intelligence)
    averages.num_ratings = str(int(averages.num_ratings) + 1)

db.session.commit()
