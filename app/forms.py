from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[DataRequired()])
    submit = SubmitField('Submit')

#-------------------------------------------------------------------------------

one_to_ten = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')]
seasons = [('Winter','Winter'),('Spring','Spring'),('Summer','Summer'),('Fall','Fall')]
years = [('2019','2019'),('2018','2018'),('2017','2017'),('2016','2016'),('2015','2015'),('2014','2014'),('2013','2013'),('2012','2012'),('2011','2011'),('2010','2010'),\
        ('2009','2009'),('2008','2008'),('2007','2007'),('2006','2006'),('2005','2005'),('2004','2004'),('2003','2003'),('2002','2002'),('2001','2001'),('2000','2000'),\
        ('1999','1999'),('1998','1998'),('1997','1997'),('1996','1996'),('1995','1995'),('1994','1994'),('1993','1993'),('1992','1992'),('1991','1991'),('1990','1990')]
ratings = [('G - All Ages','G - All Ages'), ('PG - Children','PG - Children'), ('PG-13 - Teens 13 or older','PG-13 - Teens 13 or older'),\
           ('R - 17+ (violence & profanity)','R - 17+ (violence & profanity)'), ('R+ - Mild Nudity','R+ - Mild Nudity'), ('Rx - Hentai','Rx - Hentai')]
allgenres = [('Action','Action'),('Adventure','Adventure'),('Comedy','Comedy'),('Drama','Drama'),\
             ('Demons','Demons'),('Ecchi','Ecchi'),('Fantasy','Fantasy'),('Game','Game'),\
             ('Harem','Harem'),('Hentai','Hentai'),('Historical','Historical'),('Horror','Horror'),
             ('Isekai','Isekai'),('Kids','Kids'),('Magic','Magic'),('Martial Arts','Martial Arts'),\
             ('Mecha','Mecha'),('Military','Military'),('Music','Music'),('Mystery','Mystery'),\
             ('Parody','Parody'),('Post-Apocalyptic','Post-Apocalyptic'),('Psychological','Psychological'),('Romance','Romance'),\
             ('Sci-Fi','Sci-Fi'),('Shoujo','Shoujo'),('Shounen','Shounen'),('Slice of Life','Slice of Life'),\
             ('Sports','Sports'),('Supernatural','Supernatural'),('Super Power','Super Power'),('Vampire','Vampire'),\
             ('Yaoi','Yaoi'),('Yuri','Yuri')]

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class UploadWaifuForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    anime_name = StringField('Anime Name', validators=[DataRequired()])
    tags = StringField('Tags (separate by commas)', validators=[DataRequired()])
    submit = SubmitField('Upload')

class UploadAnimeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    season = SelectField('Season', choices=seasons)
    year = SelectField('Year', choices=years)
    num_episodes = StringField('Number of Episodes', validators=[DataRequired()])
    esrb = SelectField('ESRB Rating', choices=ratings)
    description = StringField('Description', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    studio = StringField('Studio Name', validators=[DataRequired()])
    genres = MultiCheckboxField('Genres', choices=allgenres, validators=[DataRequired()])
    submit = SubmitField('Upload')

class RateWaifuForm(FlaskForm):
    appearance = SelectField("Rate this Waifu's appearance (1-10)", choices=one_to_ten)
    personality = SelectField("Rate this Waifu's personality (1-10)", choices=one_to_ten)
    strength = SelectField("Rate this Waifu's combat ability (1-10)", choices=one_to_ten)
    intelligence = SelectField("Rate this Waifu's intelligence (1-10)", choices=one_to_ten)
    wouldyou = StringField('Would you?', validators=[DataRequired()])
    body = TextAreaField('Tell us how you really feel about this Waifu.', validators=[DataRequired()])
    submit = SubmitField('Submit')
