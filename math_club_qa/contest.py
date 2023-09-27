from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from math_club_qa.auth import login_required
from math_club_qa.db import get_db

from flask import (send_file, make_response, Response)
import json
import os

bp = Blueprint('contest', __name__, url_prefix='/contest')

@bp.route('/exercise')
@login_required
def exercise():
    if g.user['userGroup'] == 'members':
        return render_template('/contest/exercise.html')
    elif g.user['userGroup'] == 'admins':
        return render_template('/contest/set.html')
    return render_template('/contest/exercise.html')

@bp.route("/set",  methods=['POST'])
@login_required
def setQuestion():
    date = request.form['date']
    if(date is None):
        return "Date is required.", 400
    dir = os.path.dirname(__file__)
    if(os.name == 'nt'):
        dir = dir + '\\' + 'contestImages\\'
    else:
        dir = dir + '/' + 'contestImages/'
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

@bp.route('/getImage', methods=['POST'])
def getImage():
    json_data = request.get_json()
    if not json_data:
        return 'Invalid JSON', 400
    date = json_data.get('date')

    imageType = 'image/png'
    dir = os.path.dirname(__file__)
    if(os.name == 'nt'):
        dir = dir + '\\' + 'ContestImages\\'
    else:
        dir = dir + '/' + 'ContestImages/'
    fileName =  date + '.png'
    existing = os.path.exists(dir + fileName)

    if(not existing):
        imageType = 'image/jpg'
        fileName = date + '.jpg'
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

