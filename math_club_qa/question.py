from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from math_club_qa.auth import login_required
from math_club_qa.db import get_db

from flask import (send_file, make_response, Response)
import json
import os

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/select')
def select():
    if g.user is None:
        return render_template('/question/select.html', totalQ=50)
    elif g.user['userGroup'] == 'members':
        return render_template('/question/exercise.html', totalQ=50)
    else:
        return render_template('/question/set.html', totalQ=50)

@bp.route('/getImage', methods=['POST'])
def getImage():
    json_data = request.get_json()
    if not json_data:
        return 'Invalid JSON', 400
    date = json_data.get('date')
    questionN = json_data.get('questionNum')

    imageType = 'image/png'
    dir = os.path.dirname(__file__)
    if(os.name == 'nt'):
        dir = dir + '\\' + 'questionImages\\'
    else:
        dir = dir + '/' + 'questionImages/'
    fileName =  date + "_" + questionN+ '.png'
    existing = os.path.exists(dir + fileName)

    if(not existing):
        imageType = 'image/jpg'
        fileName = date + "_" + questionN + '.jpg'
        existing = os.path.exists(dir + fileName)
    
    if(not existing):
        imageType = 'image/png'
        fileName ='notAvailable.png'
    response = send_file(dir + fileName, mimetype=imageType)
    if(not existing):
        response.status = 299
    else:
        response.status = 200
    return response

@bp.route("/submitAnswer",  methods=['POST'])
@login_required
def sumbitAnswer():
    json_data = request.get_json()
    if not json_data:
        return 'Invalid JSON', 400
    userId = g.user['id']
    userName = g.user['userName']
    date = json_data.get('date')
    answer = json_data.get('answer')
    sql = 'insert into userAnswers (datefor, adderId, adderName, answer) values(?, ?, ?, ?)' 
    db = get_db()
    db.execute(sql, (date, userId, userName, answer,))
    db.commit()
    
    data = {
            'answer': 'Answer submitted.'
    }
    json_data = json.dumps(data)
    response = Response(json_data, content_type='application/json')
    return response

@bp.route("/getUserAnswer",  methods=['POST'])
@login_required
def getUserAnswer():
    json_data = request.get_json()
    if not json_data:
        return 'Invalid JSON', 400
    
    date = json_data.get('date')
    sql = 'select id, dateFor, userId, answer from userAnswers where userId=? and dateFor=? order by id desc'
    db = get_db()
    row = db.execute(sql, (g.user['id'], date,)).fetchone()
    if(row is not None):
        data = {
            'answer': row['answer']
        }
        status = 200
    else:
        data = {
            'answer': ''           
        }
        status = 299
    json_data = json.dumps(data)
    response = Response(json_data, content_type='application/json')
    response.status = status
    return response

@bp.route("/set",  methods=['POST'])
@login_required
def setQuestion():
    date = request.form['date']
    if(date is None):
        return "Date is required.", 400
    dir = os.path.dirname(__file__)
    if(os.name == 'nt'):
        dir = dir + '\\' + 'questionImages\\'
    else:
        dir = dir + '/' + 'questionImages/'
    jpgExisting = os.path.exists(dir + date + '.jpg')
    pngExisting = os.path.exists(dir + date + '.png')
    existing = jpgExisting or pngExisting
    returnMessage = ''

    file = request.files['image']
    if(file is not None):
        fnEx = file.filename[-3:]

        fileName = date + '.' + fnEx
        i = 0
        jpgNewName = None
        pngNewName = None
        while existing:
            i = i + 1
            jpgNewName = dir + date + '(' + str(i) + ').jpg'
            pngNewName = dir + date + '(' + str(i) + ').png'
            existing = os.path.exists(jpgNewName) or os.path.exists(pngNewName)

        if(jpgExisting):
            os.rename(dir + date + '.jpg', jpgNewName)
        if(pngExisting):
            os.rename(dir + date + '.png',  pngNewName)
            
        open(dir + fileName, 'wb').write(file.read())
        existing = True
        returnMessage += 'File uploaded successfully. '
    if(existing):
        refAnswer = request.form['refAnswer']
        if(refAnswer is not None):
            sql = 'insert into questions(dateFor, refAnswer, setterId, setterName) values (?, ?, ?, ?)'
            db = get_db()
            db.execute(sql, (date, refAnswer, g.user['id'], g.user['userName']))
            db.commit()
            returnMessage += 'Reference answer is set.'
    else:
        returnMessage += 'A question image is required before the reference answer.'
    return returnMessage

@bp.route("/getRefAnswer",  methods=['POST'])
@login_required
def getRefAnswer():
    json_data = request.get_json()
    if not json_data:
        return 'Invalid JSON', 400
    date = json_data.get('date')

    db = get_db()
    sql = 'select id, refAnswer from questions where dateFor=? order by id desc'
    row = db.execute(sql, (date,)).fetchone()

    if(row is not None):
        data = {
            'id': row['id'],
            'refAnswer': row['refAnswer']
        }
        status = 200
    else:
        data = {
            'id': -1,
            'refAnswer': 'Not available.'
        }
        status = 299  
    json_data = json.dumps(data)
    response = Response(json_data, content_type='application/json')
    response.status = status
    return response
