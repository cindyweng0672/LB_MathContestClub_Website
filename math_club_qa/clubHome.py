from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


bp = Blueprint('home',__name__)

@bp.route('/')
@bp.route('/home')
def home():
    return render_template('clubHome.html')
