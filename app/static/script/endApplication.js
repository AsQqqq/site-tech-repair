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
                <input type="text" name="serviceWarranty[]" required placeholder="14д.">
            </div>
            <button type="button" class="cta-button" onclick="removeService('service_${serviceCount}')">Удалить услугу</button>
        `;

        serviceContainer.appendChild(newServiceBlock);
    }

    // Функция для удаления услуги
    function removeService(serviceId) {
        const serviceBlock = document.getElementById(serviceId);
        serviceBlock.remove();
        updateTotalAmount();  // Обновить общую сумму после удаления услуги
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
    }

    // Функция для обновления общей суммы
    function updateTotalAmount() {
        let totalAmount = 0;
        const serviceTotalInputs = document.querySelectorAll('[name="serviceTotal[]"]');
        serviceTotalInputs.forEach(input => {
            totalAmount += parseFloat(input.value) || 0;
        });
        document.getElementById('totalAmount').value = totalAmount.toFixed(2);  // Обновить поле общей суммы
    }

    // Функция для обновления общей суммы в поле expenseAmount
    function updateTotalAmount() {
        let totalAmount = 0;
        const serviceTotalInputs = document.querySelectorAll('[name="serviceTotal[]"]');
        serviceTotalInputs.forEach(input => {
            totalAmount += parseFloat(input.value) || 0;
        });

        // Обновляем поле expenseAmount с общей суммой
        document.getElementById('expenseAmount').value = totalAmount.toFixed(2);
    }