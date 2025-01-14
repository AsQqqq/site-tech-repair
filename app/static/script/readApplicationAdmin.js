// Функция для открытия модального окна с изображением
function openModal(imageUrl) {
    const modal = document.getElementById("modal");
    const modalImage = document.getElementById("modal-image");

    if (imageUrl) {
        modal.style.display = "flex";  // Показываем модальное окно
        modalImage.src = imageUrl;    // Устанавливаем источник изображения
    } else {
        console.error("URL изображения не передан!");
    }
}

// Функция для закрытия модального окна
function closeModal() {
    const modal = document.getElementById("modal");
    modal.style.display = "none"; // Скрываем модальное окно
}

// Закрытие модального окна при клике вне изображения
window.onclick = function(event) {
    const modal = document.getElementById("modal");
    if (event.target === modal) {
        closeModal();
    }
}

// Закрытие модального окна при нажатии клавиши Escape
window.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        closeModal();
    }
});


// Функция для проверки наличия всех 3 фотографий
function validatePhotos() {
    const photoFields = [
        document.getElementById('photoInput1'), // Чек
        document.getElementById('photoInput2'), // Лицевая сторона документа
        document.getElementById('photoInput3')  // Задняя сторона документа
    ];

    for (let i = 0; i < photoFields.length; i++) {
        if (!photoFields[i].files.length) {
            // Flash-сообщение для отображения ошибки
            flashMessage('Пожалуйста, загрузите все три фотографии: чек, лицевая и задняя сторона документа.');
            return false; // Если хотя бы одно фото не загружено, форма не будет отправлена
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
        event.preventDefault();  // Если услуг нет или не все фото загружены, блокируем отправку формы
    }
});
