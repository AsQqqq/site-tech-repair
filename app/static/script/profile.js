// Функция для открытия модального окна
function openCreateApiModal() {
    const modal = document.getElementById("create-api-modal");
    modal.style.display = "flex";  // Показываем модальное окно
}

// Функция для закрытия модального окна
function closeCreateApiModal() {
    const modal = document.getElementById("create-api-modal");
    modal.style.display = "none"; // Скрываем модальное окно
}

// Открытие модального окна при нажатии на кнопку
document.querySelector(".create-api-btn").addEventListener("click", function() {
    openCreateApiModal();
});

// Закрытие модального окна при нажатии на крестик
document.querySelector(".close").addEventListener("click", function() {
    closeCreateApiModal();
});

// Закрытие модального окна при клике вне его
window.addEventListener("click", function(event) {
    const modal = document.getElementById("create-api-modal");
    if (event.target === modal) {
        closeCreateApiModal();
    }
});

// Закрытие модального окна при нажатии клавиши Escape
window.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        closeCreateApiModal();
    }
});

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

function flashMessageSuccess(message) {
    // Отправка flash-сообщения на сервер (если вы используете Flask)
    const formData = new FormData();
    formData.append('message', message);
    
    fetch('/flash-message-success', {  // Путь, на который мы будем отправлять сообщение
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
        console.log(data); // Успешно отправлено сообщение на сервер
        location.reload();
      }).catch(err => console.error('Error sending message:', err));
}

// Отправка формы через POST запрос
document.getElementById("create-api-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Предотвращаем перезагрузку страницы

    // Получаем значения из формы
    const apiName = document.getElementById("api-name").value;
    const apiDescription = document.getElementById("api-description").value;

    // Отправка POST запроса
    fetch('/create-api-key', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: apiName,
            description: apiDescription,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            // Если ошибка в данных, показываем сообщение и перенаправляем
            flashMessage(data.error);
            window.location.href = '/profile';  // Перенаправляем на другую страницу
        } else {
            location.reload()
            flashMessageSuccess('API-ключ успешно создан!');
            // console.log('API-ключ успешно создан:', data);
            // Закрытие модального окна после успешного создания
            closeCreateApiModal();
        }
    })
    .catch((error) => {
        console.error('Ошибка при создании API-ключа:', error);
    });
});


function copyToClipboard(event) {
    const text = event.target.getAttribute('data-clipboard-text');
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    flashMessageSuccess('Скопировано в буфер обмена!');
}

let currentApiKeyId = null;


// Открытие модального окна
function openDeleteModal(apiKeyId) {
    currentApiKeyId = apiKeyId;  // Сохраняем ID ключа
    document.getElementById("confirmationModal").style.display = "flex"; // Показываем модальное окно
}

// Закрытие модального окна
function closeDeleteModal() {
    document.getElementById("confirmationModal").style.display = "none"; // Скрываем модальное окно
}

// Подтверждение удаления
document.getElementById("confirmDelete").addEventListener("click", function() {
    if (currentApiKeyId) {
        // Отправка запроса на удаление API-ключа
        fetch(`/delete-api-key/${currentApiKeyId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                flashMessageSuccess("Успешно удален API-ключ!");
                // Если удаление прошло успешно, обновим страницу
                location.reload();
            } else {
                alert("Ошибка при удалении API-ключа");
            }
        })
        .catch((error) => {
            console.error('Ошибка при удалении API-ключа:', error);
        });
    }
    closeDeleteModal();  // Закрываем модальное окно после выполнения действия
});

// Отмена удаления
document.getElementById("cancelDelete").addEventListener("click", function() {
    closeDeleteModal();  // Просто закрываем модальное окно
});

// Привязка кнопки "Удалить" к функции открытия модального окна
function deleteApiKey(apiKeyId) {
    openDeleteModal(apiKeyId);  // Открываем модальное окно с переданным ID
}