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
  
  async function fetchImage(pickedDate, questionN, category) {
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
          const imageDisplayElement=category+"-img"
          const imageElement = document.getElementById(imageDisplayElement);
          imageElement.src = imageUrl;
        };
    }
    return response.status;
  }
  
  async function fetchUserAnswer(pickedDate) {
      const response = await fetch('/question/getUserAnswer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          date: pickedDate
        })
      });
      if(!response.ok)
        return response.status;
  
      const data = await response.json();
      const refAnswerElem = document.getElementById("answer");
      refAnswerElem.value = data['answer'];
      return response.status;
  }
  
  async function fetchRefAnswer(pickedDate){
    const response = await fetch('/question/getRefAnswer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          date: pickedDate
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
      submitButton.disabled = true;
    }
    
   
    return response.status;
  }
  
  
  function setQuestion(category, questionNum){
    date = document.getElementById("datePicker").value;
    refAnswer = document.getElementById("refAnswer").value;
    refAnswer = refAnswer.trim();
    refAnswer = refAnswer.toLowerCase();
    file = document.getElementById("imageFile").files[0];
    if(refAnswer == "" || file == undefined)
        return;
    
    const formData = new FormData();
    formData.append('date', date);
    formData.append('refAnswer', refAnswer);
    formData.append('image', file);
    formData.append('questionN', questionNum);
    // Send the POST request
    const tabChoice='/'+category+'/set'
    fetch(tabChoice, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // File uploaded successfully
            console.log('File uploaded');
            centerDate = new Date();
            year = date.substring(0,4);
            month = date.substring(5, 7) - 1
            day = date.substring(8, 10)
            centerDate.setFullYear(year, month, day);
            date_picking_callback_set(centerDate);
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
  
  
  function submitAnwser(){
    answer = document.getElementById("answer").value;
    date= document.getElementById("datePicker").value;
    answer = answer.trim();
    answer = answer.toLowerCase(answer);
  
    if(answer == '')
      return;
    fetch('/question/submitAnswer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            date: date,
            answer: answer
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        fetchRefAnswer(date);
    })
    .catch(error => {
        console.error('Error:', error);
    });
  }
  