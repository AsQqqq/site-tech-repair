let serviceCount = 1;  // Счётчик для услуг

// Функция для добавления новой услуги
function addService() {
    serviceCount++;
    const serviceContainer = document.getElementById('servicesContainer');

    const newServiceBlock = document.createElement('div');
    newServiceBlock.classList.add('service-block');
    newServiceBlock.id = `service_${serviceCount}`;

    newServiceBlock.innerHTML = `
        <div class="form-group">
            <label for="serviceName">Наименование услуги</label>
            <input type="text" name="serviceName[]" required>
        </div>
        <div class="form-group">
            <label for="servicePrice">Цена</label>
            <input type="number" name="servicePrice[]" min="0" step="0.01" required oninput="calculateServiceSum(this)">
        </div>
        <div class="form-group">
            <label for="serviceQuantity">Кол-во</label>
            <input type="number" name="serviceQuantity[]" min="0" step="1" required oninput="calculateServiceSum(this)">
        </div>
        <div class="form-group">
            <label for="serviceTotal">Сумма</label>
            <input type="number" name="serviceTotal[]" min="0" step="0.01" required readonly placeholder="Сумма услуги">
        </div>
        <div class="form-group">
            <label for="serviceWarranty">Гарантия</label>
            <input class="servicewrrnt" type="text" name="serviceWarranty[]" required placeholder="14д.">
        </div>
        <button type="button" class="cta-button" onclick="removeService('service_${serviceCount}')">Удалить услугу</button>
    `;

    serviceContainer.appendChild(newServiceBlock);
    checkFormValidity();  // Проверяем форму после добавления услуги
}

// Функция для удаления услуги
function removeService(serviceId) {
    const serviceBlock = document.getElementById(serviceId);
    serviceBlock.remove();
    updateTotalAmount();  // Обновить общую сумму после удаления услуги
    checkFormValidity();  // Проверяем форму после удаления услуги
}

// Функция для подсчета суммы каждой услуги
function calculateServiceSum(element) {
    const serviceBlock = element.closest('.service-block');
    const price = parseFloat(serviceBlock.querySelector('[name="servicePrice[]"]').value) || 0;
    const quantity = parseFloat(serviceBlock.querySelector('[name="serviceQuantity[]"]').value) || 0;
    const total = price * quantity;
    
    // Обновление поля "Сумма"
    serviceBlock.querySelector('[name="serviceTotal[]"]').value = total.toFixed(2);

    updateTotalAmount();  // Обновить общую сумму после изменения
    checkFormValidity();  // Проверяем форму после изменения услуги
}

// Функция для обновления общей суммы
function updateTotalAmount() {
    let totalAmount = 0;
    const serviceTotalInputs = document.querySelectorAll('[name="serviceTotal[]"]');
    serviceTotalInputs.forEach(input => {
        totalAmount += parseFloat(input.value) || 0;
    });

    // Обновляем поле expenseAmount с общей суммой
    document.getElementById('expenseAmount').value = totalAmount.toFixed(2);
}

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

// Функция для проверки наличия хотя бы одной услуги
function validateServices() {
    const serviceBlocks = document.querySelectorAll('.service-block');
    if (serviceBlocks.length === 0) {
        // Flash-сообщение для отображения ошибки
        flashMessage('Пожалуйста, добавьте хотя бы одну услугу перед отправкой заявки.');
        return false; // Если услуг нет, форма не будет отправлена
    }
    return true; // Если услуги есть, форма будет отправлена
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
    if (!validateServices() || !validatePhotos()) {
        event.preventDefault();  // Если услуг нет или не все фото загружены, блокируем отправку формы
    }
});
