from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from math_club_qa.auth import login_required
from math_club_qa.db import get_db
from math_club_qa.questionUtility import *

from flask import (send_file, make_response, Response)
import os, json


bp = Blueprint('daily', __name__, url_prefix='/daily')

@bp.route('/')
@bp.route('/start')
def start():
    if g.user is None:
        return render_template('/daily/browse.html')
    elif g.user['group'] == 'members':
        return render_template('/daily/exercise.html')
    else:
        return render_template('/daily/set.html')

@bp.route('/getImage', methods=['POST'])
def getImage():
    return getImageFun(request, 'daily')

@bp.route("/submitAnswer",  methods=['POST'])
@login_required
def sumbitAnswer():
    return submitAnswerFun(request, 'daily')

@bp.route("/getUserAnswer",  methods=['POST'])
@login_required
def getUserAnswer():
    return getUserAnswerFun(request, 'daily')

@bp.route("/setQuestion",  methods=['POST'])
@login_required
def setQuestion():
    return setQuestionFun(request, 'daily')

@bp.route("/getRefAnswer",  methods=['POST'])
@login_required
def getRefAnswer():
    return getRefAnswerFun(request, 'daily')
