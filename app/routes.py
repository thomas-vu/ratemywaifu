from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm, UploadWaifuForm, UploadAnimeForm, RateWaifuForm
from app.models import User, Post, Waifu, PendingWaifu, Anime, PendingAnime, Rating
from app.email import send_password_reset_email


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    #form = PostForm()
    #if form.validate_on_submit():
    #    post = Post(body=form.post.data, author=current_user)
    #    db.session.add(post)
    #    db.session.commit()
    #    flash('Your post is now live!')
    #    return redirect(url_for('index'))

    #page = request.args.get('page', 1, type=int)
    #posts = current_user.followed_posts().paginate(
    #    page, app.config['POSTS_PER_PAGE'], False)
    #next_url = url_for('index', page=posts.next_num) \
    #    if posts.has_next else None
    #prev_url = url_for('index', page=posts.prev_num) \
    #    if posts.has_prev else None

    ratings = Rating.query.all()

    #return render_template('index.html', title='Home', form=form,
    #                       posts=posts.items, next_url=next_url,
    #                       prev_url=prev_url, Waifu=Waifu, ratings=ratings)

    return render_template('index.html', title='Home', Waifu=Waifu, ratings=ratings)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)

    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None

    ratings = user.ratings.order_by(Rating.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=ratings.next_num) \
        if ratings.has_next else None
    prev_url = url_for('user', username=user.username, page=ratings.prev_num) \
        if ratings.has_prev else None

    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, Waifu=Waifu, ratings=ratings.items)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

#-------------------------------------------------------------------------------

@app.route('/waifus')
def browse_waifus():
    waifus = Waifu.query.all()
    return render_template('browse_waifus.html', waifus=waifus, Anime=Anime)


@app.route('/waifus/<url>')
def waifus(url):
    waifu = Waifu.query.filter_by(url=url).first_or_404()
    ratings = Rating.query.filter_by(waifu_id=waifu.id)
    return render_template('waifu.html', waifu=waifu, Waifu=Waifu, Anime=Anime, ratings=ratings)


@app.route('/anime')
def browse_anime():
    animes = Anime.query.all()
    return render_template('browse_anime.html', animes=animes)


@app.route('/anime/<url>')
def anime(url):
    anime = Anime.query.filter_by(url=url).first_or_404()
    return render_template('anime.html', anime=anime)


@app.route('/upload/<category>', methods=['GET', 'POST'])
def upload(category):
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    if category == 'waifu':
        form = UploadWaifuForm()
        if form.validate_on_submit():
            pending_waifu = PendingWaifu(name=form.name.data, description=form.description.data, \
                image=form.image.data, url=form.url.data, anime_name=form.anime_name.data)
            db.session.add(pending_waifu)
            db.session.commit()
            flash('Congratulations, you make a Waifu! (Acceptance Pending)')
            return redirect(url_for('browse_waifus'))
    elif category == 'anime':
        form = UploadAnimeForm()
        if form.validate_on_submit():
            pending_anime = PendingAnime(name=form.name.data, season=form.season.data, year=form.year.data, \
                num_episodes=form.num_episodes.data, esrb=form.esrb.data, description=form.description.data, \
                image=form.image.data, url=form.url.data)
            db.session.add(pending_anime)
            db.session.commit()
            flash('Congratulations, you make a Anime! (Acceptance Pending)')
            return redirect(url_for('browse_anime'))

    return render_template('upload.html', title=f'Upload {category.capitalize()}', form=form)


@app.route('/rate/<url>', methods=['GET', 'POST'])
def rate(url):
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    waifu = Waifu.query.filter_by(url=url).first_or_404()
    form = RateWaifuForm()
    if form.validate_on_submit():
        rating = Rating(appearance=form.appearance.data, personality=form.personality.data, \
            strength=form.strength.data, intelligence=form.intelligence.data, wouldyou=form.wouldyou.data, \
            body=form.body.data, author=current_user, rated=waifu)
        db.session.add(rating)
        db.session.commit()
        flash('Congratulations, you rate a Waifu!')
        return redirect(url_for('waifus', url=url))
    return render_template('rate.html', form=form, waifu=waifu)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.is_authenticated and current_user.admin_flag:
        pending_waifus = PendingWaifu.query.all()
        pending_animes = PendingAnime.query.all()
        return render_template('admin.html', pending_waifus=pending_waifus, pending_animes=pending_animes)
    return redirect(url_for('index'))


@app.route('/admin/<status>/<category>/<url>', methods=['GET', 'POST'])
@login_required
def admin_judgement(status, category, url):
    if current_user.is_authenticated and current_user.admin_flag:
        if status == 'accept':
            if category == 'waifu':
                pending = PendingWaifu.query.filter_by(url=url).first_or_404()
                accepted = Waifu(name=pending.name, description=pending.description, \
                    image=pending.image, url=pending.url, anime_name=pending.anime_name)
            elif category == 'anime':
                pending = PendingAnime.query.filter_by(url=url).first_or_404()
                accepted = Anime(name=pending.name, season=pending.season, year=pending.year, \
                    num_episodes=pending.num_episodes, esrb=pending.esrb, description=pending.description, \
                    image=pending.image, url=pending.url)
            db.session.add(accepted)
            db.session.delete(pending)
        elif status == 'reject':
            if category == 'waifu':
                rejected = PendingWaifu.query.filter_by(url=url).first_or_404()
            elif category == 'anime':
                rejected = PendingAnime.query.filter_by(url=url).first_or_404()
            db.session.delete(rejected)
        db.session.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('index'))
