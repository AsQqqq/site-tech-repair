function contactUs() {
    if (window.innerWidth <= 768) {
        // Для мобильных устройств инициируем звонок
        window.location.href = "tel:89155222006";
        
    } else {
        // Для ПК показываем номер телефона в модальном окне
        document.getElementById('modal').classList.add('show');
    }
}

function closeModal() {
    if (document.getElementById('modal').classList.contains('show')) {
        document.getElementById('modal').classList.remove('show');
    }
}

// Функция для отображения сообщения Flash
function flashMessage(message, type) {
    // Отправка flash-сообщения на сервер (если вы используете Flask)
    const formData = new FormData();
    formData.append('message', message);
    
    if (type == "error") {
        fetch('/flash-message', {  // Путь, на который мы будем отправлять сообщение
            method: 'POST',
            body: formData
        }).then(response => response.json())
        .then(data => {
            console.log(data); // Успешно отправлено сообщение на сервер
            location.reload();
        }).catch(err => console.error('Error sending message:', err));
    } else {
        fetch('/flash-message-success', {  // Путь, на который мы будем отправлять сообщение
            method: 'POST',
            body: formData
        }).then(response => response.json())
        .then(data => {
            console.log(data); // Успешно отправлено сообщение на сервер
            location.reload();
        }).catch(err => console.error('Error sending message:', err));
    }
}

function develop() {
    flashMessage('Изменения в разработке...', 'success');
}