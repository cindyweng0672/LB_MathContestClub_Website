from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


bp = Blueprint('activities',__name__)

@bp.route('/')
@bp.route('/activities')
def activities():
    return render_template('activities.html')