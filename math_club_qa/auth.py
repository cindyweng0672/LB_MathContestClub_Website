import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from math_club_qa.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None

        if not userName:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                    (userName, generate_password_hash(password), email),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {userName} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
        return render_template('auth/register.html', userName=userName, email=email)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        userName = request.form['userName']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE userName = ?', (userName,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('home'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/update', methods=('GET', 'POST'))
@login_required
def update():
    if request.method == 'POST':
        feedBack = 'Update succeeded.'

        password = request.form['password']
        email = request.form['email']
        password = password.strip()
        email = email.strip()

        currentPassword = request.form['currentPassword']
        currentPassword = currentPassword.strip()
        length = len(currentPassword)
        if(length == 0):
            feedBack="Current password is required."
            flash(feedBack)
            return render_template('auth/update.html', email=email)
        
        if not check_password_hash(g.user['password'], currentPassword):
            feedBack="Current password is not matched."
            flash(feedBack)
            return render_template('auth/update.html', email=email)
                    
        emailLength = len(email)
        passwordLength = len(password)

        if(passwordLength == 0 and emailLength == 0):
            return render_template('auth/update.html', email=email)
        setSql = 'update users set'

        if(passwordLength != 0):
            setSql += ' password=\'' + generate_password_hash(password) + '\''

        if(emailLength != 0):
            if(passwordLength > 0):
                setSql += ','
            setSql += ' email=\'' + email + '\' '
        setSql += " where id = " + str(g.user['id'])

        db = get_db()
        try:
            db.execute(setSql)
            db.commit()
        except db.IntegrityError:
            feedBack = 'Update failed.'
        flash(feedBack)
        load_logged_in_user()
    return render_template('auth/update.html')    


@bp.route("/search",  methods=('GET', 'POST'))
@login_required
def search():
    users = None
    if request.method == 'POST':
        userName = request.form['userName']
        email = request.form['email']
        userGroup = request.form['userGroup']
        filterCondition = ''
        if(userName != ''):
            filterCondition += 'userName=\'' + userName + '\''
        if(email != ''):
            if(filterCondition != ''):
                filterCondition += ' and '
            filterCondition += 'email=\'' + email + '\''
        if(userGroup != ''):
            if(filterCondition != ''):
                filterCondition += ' and '
            filterCondition += 'userGroup=\'' + userGroup + '\''
        sql = 'SELECT id, userName, email, userGroup, registeringTime, deactivatingTime' \
              ' FROM users'
        if(filterCondition != ""):
           sql += " WHERE " + filterCondition
        sql += ' ORDER BY id DESC'
        db = get_db()
        usersCursor = db.execute(sql)
        users = usersCursor.fetchall()
    if(users is not None):
        return render_template('auth/search.html', users=users)
    else:
        return render_template('auth/search.html')
    
      