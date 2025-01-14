document.getElementById('receiptFile').addEventListener('change', function(event) {
    var fileName = event.target.files.length > 0 ? event.target.files[0].name : '';
    document.getElementById('fileName').textContent = fileName;
});



// Функция для проверки наличия всех 3 фотографий
function validatePhotos() {
    const photoFields = [
        document.getElementById('photoInput1')
    ];

    for (let i = 0; i < photoFields.length; i++) {
        if (!photoFields[i].files.length) {
            flashMessage('Пожалуйста, прикрепите чек');
            return false;
        }
    }
    return true; // Если все фото загружены, форма будет отправлена
}


// Функция для отображения сообщения Flash
function flashMessage(message) {
    // Отправка flash-сообщения на сервер (если вы используете Flask)
    const formData = new FormData();
    formData.append('message', message);
    
    fetch('/flash-message', {  // Путь, на который мы будем отправлять сообщение
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
        console.log(data); // Успешно отправлено сообщение на сервер
        location.reload();
      }).catch(err => console.error('Error sending message:', err));
}

// Добавляем обработчик на кнопку "Отправить"
document.getElementById('saveButton').addEventListener('click', function(event) {
    if (!validatePhotos()) {
        event.preventDefault();
    }
});
