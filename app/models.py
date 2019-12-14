from datetime import datetime
from hashlib import md5
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import app, db, login

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    ratings = db.relationship('Rating', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    admin_flag = db.Column(db.Boolean)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Waifu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(5000))
    image = db.Column(db.String(140))
    url = db.Column(db.String(140))
    rating = db.relationship('Rating', backref='rated', lazy='dynamic')
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'))
    def __repr__(self):
        return '<Waifu {}>'.format(self.name)

class PendingWaifu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(5000))
    image = db.Column(db.String(140))
    url = db.Column(db.String(140))
    anime_name = db.Column(db.String(140))
    def __repr__(self):
        return '<Pending Waifu {}>'.format(self.name)

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    season = db.Column(db.String(140))
    year = db.Column(db.String(140))
    num_episodes = db.Column(db.String(140))
    esrb = db.Column(db.String(140))
    description = db.Column(db.String(5000))
    image = db.Column(db.String(140))
    url = db.Column(db.String(140))
    studio = db.Column(db.String(140))
    waifu = db.relationship('Waifu', backref='has_waifu', lazy='dynamic')
    def __repr__(self):
        return '<Anime {}>'.format(self.name)

class PendingAnime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    season = db.Column(db.String(140))
    year = db.Column(db.String(140))
    num_episodes = db.Column(db.String(140))
    esrb = db.Column(db.String(140))
    description = db.Column(db.String(5000))
    image = db.Column(db.String(140))
    url = db.Column(db.String(140))
    studio = db.Column(db.String(140))
    def __repr__(self):
        return '<Pending Anime {}>'.format(self.name)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appearance = db.Column(db.String(140))
    personality = db.Column(db.String(140))
    strength = db.Column(db.String(140))
    intelligence = db.Column(db.String(140))
    wouldyou = db.Column(db.String(140))
    body = db.Column(db.String(5000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    waifu_id = db.Column(db.Integer, db.ForeignKey('waifu.id'))
    def __repr__(self):
        return '<Rating {}>'.format(self.body)

class Studio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    def __repr__(self):
        return '<Studio {}>'.format(self.name)

class AnimeGenres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime_name = db.Column(db.String(140))
    genre = db.Column(db.String(140))
    def __repr__(self):
        return '<AnimeGenres {}>'.format(self.name)

class WaifuTags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waifu_name = db.Column(db.String(140))
    tag = db.Column(db.String(140))
    def __repr__(self):
        return '<WaifuTags {}>'.format(self.name)

class WaifuAverages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    waifu_id = db.Column(db.Integer, db.ForeignKey('waifu.id'))
    appearance_total = db.Column(db.String(140))
    personality_total = db.Column(db.String(140))
    strength_total = db.Column(db.String(140))
    intelligence_total = db.Column(db.String(140))
    num_ratings = db.Column(db.String(140))
    def __repr__(self):
        return '<WaifuAverages {}>'.format(self.name)
