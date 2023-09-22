
  
  function setContestQuestion(){
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
    // Send the POST request
    fetch('/contest/set', {
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

  async function fetchContestImage(pickedDate) {
    const response = await fetch('/contest/getImage', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        date: pickedDate
      })
    });
    if(response.ok){
        const contentType = response.headers.get("Content-Type");
        if(contentType.includes('image')){
          const blob = await response.blob();
          const imageUrl = URL.createObjectURL(blob);
          const imageElement = document.getElementById("contest-img");
          imageElement.src = imageUrl;
        };
    }
    return response.status;
  }
  

  
  