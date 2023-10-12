import os, json, time
from math_club_qa.db import get_db
from flask import (g, send_file, request, make_response, Response)

def getImageFileNameHeader(date, questionNum, category):
    suffix = 'd'
    if(category != 'daily'):
        suffix = 'c'
    fileNameHeader =  date + '_' + str(questionNum) + '_' + suffix
    return fileNameHeader

def getImageFolderName():
    dir = os.path.dirname(__file__)
    if(os.name == 'nt'):
        dir = dir + '\\' + 'questionImages\\'
    else:
        dir = dir + '/' + 'questionImages/'
    return dir

def getImageFileName(date, questionNum, category):
    dir = getImageFolderName()
    fileNameHeader = getImageFileNameHeader(date, questionNum, category)
    fileName = fileNameHeader + '.png'
    existing = os.path.exists(dir + fileName)

    if(not existing):
        fileName = fileNameHeader + ".jpg"
        existing = os.path.exists(dir + fileName)
    
    if(not existing):
        fileName ='notAvailable.png'
    return dir + fileName

def renameCurrentQuestionImage(date, questionNum, category):
    dir = getImageFolderName()
    fileNameHeader = getImageFileNameHeader(date, questionNum, category)
    fileName = getImageFileName(date, questionNum, category)
    jpgExisting = False
    pngExisting = False
    if(fileName.find('notAvailable') < 0):
        fileNameExt = fileName[-3:]
        if(fileNameExt == 'jpg' or fileNameExt == "JPG"):
            jpgExisting = True
        else:
            pngExisting = True
    fileNameHeader = dir + fileNameHeader
    i = 0
    jpgNewName = None
    pngNewName = None
    existing = jpgExisting or pngExisting
    while existing:
        i = i + 1
        jpgNewName = fileNameHeader + '(' + str(i) + ').jpg'
        pngNewName = fileNameHeader + '(' + str(i) + ').png'
        existing = os.path.exists(jpgNewName) or os.path.exists(pngNewName)

    if(jpgExisting):
        os.rename(fileNameHeader + '.jpg', jpgNewName)
    if(pngExisting):
        os.rename(fileNameHeader + '.png', pngNewName)
    return fileNameHeader

def getImageFun(request, category):
    json_data = request.get_json()
    if not json_data:
        return 'Invalid JSON', 400
    date = json_data.get('date')
    questionN = 1
    if(category != 'daily'):
        questionN = json_data.get('questionNum')

    fileName = getImageFileName(date, questionN, category)
    extensionName = fileName[-3:]
    imageType = 'image/' + extensionName
    response = send_file(fileName, mimetype=imageType)
    if(fileName.find("notAvailable") > 0):
        response.status = 299
    else:
        response.status = 200
    return response

def setQuestionFun(request, category):
    date = request.form['date']
    if(date is None):
        return "Date is required.", 400
    questionNum = 1
    if(category != 'daily'):
        questionNum = request.form['questionNum']
    if(questionNum is None):
        return "Question Number is required.", 400
    returnMessage = ''
    existing = False
    fileName = getImageFileName(date, 'daily', questionNum)
    if(fileName.find('notAvailable') < 0):
        existing = True
    file = request.files['image']
    if(file is not None):
        if(existing):
            fileNameHeader = renameCurrentQuestionImage(date, questionNum, category)
            fileName = fileNameHeader + '.' + file.filename[-3:]
        else:
            dir = getImageFolderName()
            fileNameExt = file.filename[-3:]
            fileName = dir + getImageFileNameHeader(date, questionNum, category) + '.' + fileNameExt
        open(fileName, 'wb').write(file.read())
        existing = True
        returnMessage += 'File uploaded successfully. '
    if(existing):
        refAnswer = request.form['refAnswer']
        if(refAnswer is not None):
            tableName = category + 'Questions'
            db = get_db()    
            sql = 'update ' + tableName + ' set deactivatingTime = ? where date = ? and questionNum = ?;'
            now = time.localtime()
            currentTime = time.strftime('%Y-%m-%d %H:%M:%S', now)
            db.execute(sql, (currentTime, date, questionNum))
            sql = 'insert into ' + tableName + '(date, questionNum, refAnswer, userId, userName) values (?, ?, ?, ?, ?);'
            db.execute(sql, (date, questionNum, refAnswer, g.user['id'], g.user['userName']))
            db.commit()
            returnMessage += 'Reference answer is set.'
    else:
        returnMessage += 'A question image is required before the reference answer.'
    return returnMessage, 200    

def submitAnswerFun(request, category):
    json_data = request.get_json()
    if not json_data:
        return 'Invalid JSON', 400
    userId = g.user['id']
    userName = g.user['userName']
    date = json_data.get('date')
    questionNum = 1
    if(category != 'daily'):
        questionNum = json_data.get('questionNum')
    answer = json_data.get('answer')

    tableName = category + 'UserAnswers'

    db = get_db()
    sql = 'delete from ' + tableName + ' where userId = ? and date = ? and questionNum = ?' 
    db.execute(sql, (userId, date, questionNum,))

    sql = 'insert into ' + tableName + '(date, questionNum, userId, userName, answer) values(?, ?, ?, ?, ?)' 
    db.execute(sql, (date, questionNum, userId, userName, answer,))

    db.commit()
    data = {
            "answer": 'Answer submitted.'
    }
    json_data = json.dumps(data)
    response = Response(json_data, content_type='application/json')
    return response

def getUserAnswerFun(request, category):
    json_data = request.get_json()
    if not json_data:
        return 'Invalid JSON', 400
    date = json_data.get('date')
    questionNum = 1
    if(category != 'daily'):
        questionNum = json_data.get('questionNum')
    tableName = category + 'UserAnswers'

    sql = 'select id, date, questionNum, userId, answer from ' + tableName + ' where userId=? and date=? and questionNum=? order by id desc'
    db = get_db()
    row = db.execute(sql, (g.user['id'], date, questionNum)).fetchone()
    if(row is not None):
        data = {
            "answer": row['answer']
        }
        status = 200
    else:
        data = {
            "answer": ''           
        }
        status = 299
    json_data = json.dumps(data)
    response = Response(json_data, content_type='application/json')
    response.status = status
    return response    


def getRefAnswerFun(request, category):
    json_data = request.get_json()
    if not json_data:
        return 'Invalid JSON', 400
    date = json_data.get('date')
    questionNum = json_data.get('questionNum')

    db = get_db()
    tableName = category + 'Questions'
    sql = 'select id, refAnswer from ' + tableName + ' where date=? and questionNum=? order by id desc'
    row = db.execute(sql, (date, questionNum)).fetchone()

    if(row is not None):
        data = {
            "id": row['id'],
            "refAnswer": row['refAnswer']
        }
        status = 200
    else:
        data = {
            "id": -1,
            "refAnswer": 'Not available.'
        }
        status = 299  
    json_data = json.dumps(data)
    response = Response(json_data, content_type='application/json')
    response.status = status
    return response
