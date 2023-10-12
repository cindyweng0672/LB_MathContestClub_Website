function assembleDate(d){
    pickedDate = new Date(d)
    let day = pickedDate.getDate();
    let month = pickedDate.getMonth();
    month += 1;
    let year = pickedDate.getFullYear();
    dateString = year + '-'
    if(month < 10)
      dateString += '0';
    dateString += month + "-"
    if(day < 10)
      dateString += '0';
    dateString += day;
    return dateString;
  }
  
  async function getImage(pickedDate, questionN, category) {
    const functionChoice='/'+category+'/getImage'
    const response = await fetch(functionChoice, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        date: pickedDate,
        questionNum: questionN
      })
    });
    if(response.ok){
        const contentType = response.headers.get("Content-Type");
        if(contentType.includes('image')){
          const blob = await response.blob();
          const imageUrl = URL.createObjectURL(blob);
          const imageDisplayElement="question-img"
          const imageElement = document.getElementById(imageDisplayElement);
          imageElement.src = imageUrl;
          imageElement.textContent = response.status;
        };
    }
    return response.status;
  }
  
  async function getUserAnswer(date, questionNum, category) {
      urlStr = '/' + category + '/getUserAnswer'
      const response = await fetch(urlStr, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          date: date,
          questionNum: questionNum
        })
      });
      if(!response.ok)
        return response.status;
  
      const data = await response.json();
      const answerElem = document.getElementById("answer");
      answerElem.value = data['answer'];
      return response.status;
  }
  
  async function getRefAnswer(pickedDate, questionNum, category){
    const response = await fetch('/' +category + '/getRefAnswer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          date: pickedDate,
          questionNum: questionNum
        })
    });
    if(!response.ok)
      return response.status
  
    const data = await response.json();
    refAnswerElem = document.getElementById("refAnswer");
    if(refAnswerElem.tagName == 'INPUT'){
      if(response.status == 200)
        refAnswerElem.value = data['refAnswer'];
      else
        refAnswerElem.value = '';
    }
    else{
      refAnswerElem.textContent = data['refAnswer'];
      submitButton = document.getElementById('submit');
      if(response.status == 200)
        submitButton.disabled = true;
      else
        submitButton.disabled = false;
    }
   
    return response.status;
  }
  
  
  function setQuestion(questionNum, category){
    date = undefined
    if(category == 'daily')
      date = document.getElementById("datePicker").value;
    else
      date = document.getElementById("contestDate").textContent;
    refAnswer = document.getElementById("refAnswer").value;
    refAnswer = refAnswer.trim();
    refAnswer = refAnswer.toLowerCase();
    file = document.getElementById("imageFile").files[0];
    if(refAnswer == "" || file == undefined)
        return;
    
    const formData = new FormData();
    formData.append('date', date);
    formData.append('refAnswer', refAnswer);
    formData.append('questionNum', questionNum);
    formData.append('image', file);
    // Send the POST request
    const tabChoice='/'+category+'/setQuestion'
    fetch(tabChoice, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // File uploaded successfully
            console.log('File uploaded');
            if(category == 'daily'){
              centerDate = new Date();
              year = date.substring(0,4);
              month = date.substring(5, 7) - 1
              day = date.substring(8, 10)
              centerDate.setFullYear(year, month, day);
              date_picking_callback(centerDate);
            }else{
              elements = document.getElementsByClassName('selected');
              for (i = 0; i < elements.length; i++) {
                if(elements[i].tagName == 'LI')
                  selectQuestion(elements[i]);
              }   
            }
            submitButton = document.getElementById('submit');
            submitButton.disabled = true;
        } else {
            // Error handling
            console.error('File upload failed');
        }
        })
    .catch(error => {
        console.error('Error:', error);
    });
  } 
  
  
  function submitAnwser(questionNum, category){
    answer = document.getElementById("answer").value;
    date = undefined;
    if(category == 'daily')
      date = document.getElementById("datePicker").value;
    else
      date = document.getElementById("contestDate").textContent;
    answer = answer.trim();
    answer = answer.toLowerCase(answer);

    if(answer == '')
      return;
    fetch('/' + category + '/submitAnswer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            date: date,
            questionNum: questionNum,
            answer: answer
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if(category == 'daily')
          getRefAnswer(date, questionNum, category);
    })
    .catch(error => {
        console.error('Error:', error);
    });
  }
  