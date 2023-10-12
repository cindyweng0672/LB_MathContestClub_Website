from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from math_club_qa.auth import login_required
from math_club_qa.db import get_db
from math_club_qa.questionUtility import *

from flask import (send_file, make_response, Response)
from datetime import(datetime, timedelta)
import os, json

bp = Blueprint('contest', __name__, url_prefix='/contest')

@bp.route('/start')
@login_required
def start():
    #for debug.
    #return render_template('/contest/make.html', totalQ=15, date = '2023-10-23')
    #return render_template('/contest/take.html', totalQ=15, date = '2023-10-23', leftTime = "2023-11-01 03:20:20")

    db = get_db()
    contests = db.execute(
            'SELECT * FROM contests order by id desc'
        ).fetchall()
    if(g.user['group'] == 'members'):   
        return render_template('/contest/startTaking.html', contests=contests)
    else:
        return render_template('/contest/startMaking.html', contests=contests)

@bp.route('/take', methods=['POST'])
@login_required
def take():
    date = request.form['date']
    leftTime = request.form['leftTime']
    return render_template('/contest/take.html', totalQ=15, date = date, leftTime = leftTime)


@bp.route('/make', methods=['POST'])
@login_required
def make():
    date = request.form['date']
    return render_template('/contest/make.html', totalQ=15, date = date)


@bp.route('/getImage', methods=['POST'])
def getImage():
    return getImageFun(request, 'contest')

@bp.route("/submitAnswer",  methods=['POST'])
@login_required
def sumbitAnswer():
    return submitAnswerFun(request, 'contest')

@bp.route("/getUserAnswer",  methods=['POST'])
@login_required
def getUserAnswer():
    return getUserAnswerFun(request, 'contest')

@bp.route("/setQuestion",  methods=['POST'])
@login_required
def setQuestion():
    return setQuestionFun(request, 'contest')

@bp.route("/getRefAnswer",  methods=['POST'])
@login_required
def getRefAnswer():
    return getRefAnswerFun(request, 'contest')

@bp.route('/logStartTime', methods=['POST'])
def logStartTime():
    json_data = request.get_json()
    if not json_data:
        return 'Invalid JSON', 400
    date = json_data.get('date')
    userId = g.user['id']
    userName = g.user['userName']
    endTime = logStartTimeFun(userId, userName, date)
    return endTime

def logStartTimeFun(userId, userName, date):
    db = get_db()
    log = db.execute(
        'SELECT * FROM contestUserLog WHERE userId = ? and contestDate = ?', (userId, date)
    ).fetchone()
    if log is None:
        startTime=datetime.now()
        endTime=datetime.now() + timedelta(hours=3)
        sql = 'insert into contestUserLog (userId, userName, contestDate, startTime, endTime) values(?, ?, ?, ?, ?)' 
        db = get_db()
        db.execute(sql, (userId, userName, date, startTime, endTime))
        db.commit()
        return endTime.strftime("%Y-%m-%d %H:%M:%S")
    else:
        startTime = log['startTime']
        endTime = log['endTime']
        return endTime