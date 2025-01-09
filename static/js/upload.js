// Функция для добавления нового блока услуги
function addService() {
    const serviceContainer = document.getElementById('services-container');
    const newService = document.createElement('div');
    newService.classList.add('service-block');
    newService.innerHTML = `
        <label for="service_name">Услуга:</label>
        <input type="text" name="services[]" required><br><br>
        
        <label for="service_price">Цена:</label>
        <input type="number" name="prices[]" class="service-price" required><br><br>

        <label for="service_quantity">Количество:</label>
        <input type="number" name="quantities[]" class="service-quantity" min="1" required><br><br>

        <label for="service_sum">Сумма:</label>
        <input type="text" name="sums[]" class="service-sum" readonly><br><br>

        <label for="service_warranty">Гарантия:</label>
        <input type="text" name="warranties[]" required><br><br>

        <button type="button" onclick="removeService(this)">Удалить услугу</button><br><br>
    `;
    serviceContainer.appendChild(newService);

    // Добавляем обработчики для новых элементов
    const priceInput = newService.querySelector('.service-price');
    const quantityInput = newService.querySelector('.service-quantity');
    const sumInput = newService.querySelector('.service-sum');

    // Обработчики изменения данных в поле количества или цены
    priceInput.addEventListener('input', updateServiceSum);
    quantityInput.addEventListener('input', updateServiceSum);
    
    // Убедимся, что обновление итогов происходит
    priceInput.addEventListener('input', updateTotals);
    quantityInput.addEventListener('input', updateTotals);
    sumInput.addEventListener('input', updateTotals);

    // Обновляем итоги при добавлении новой услуги
    updateTotals();
}

// Функция для удаления блока услуги
function removeService(button) {
    const serviceBlock = button.closest('.service-block');
    serviceBlock.remove();
    updateTotals();  // Обновляем итоги при удалении услуги
}

// Функция для обновления суммы каждой услуги
function updateServiceSum() {
    const serviceBlock = this.closest('.service-block');
    const priceInput = serviceBlock.querySelector('.service-price');
    const quantityInput = serviceBlock.querySelector('.service-quantity');
    const sumInput = serviceBlock.querySelector('.service-sum');

    const price = parseFloat(priceInput.value) || 0;
    const quantity = parseFloat(quantityInput.value) || 0;

    // Обновляем сумму услуги (Цена * Количество)
    const sum = price * quantity;
    sumInput.value = sum.toFixed(2);

    updateTotals();  // Обновляем общие итоги
}

// Функция для обновления итогов стоимости
function updateTotals() {
    let totalCost = 0;
    let discount = parseFloat(document.getElementById('discount').value) || 0;
    const serviceSums = document.getElementsByName('sums[]');

    // Суммируем все услуги
    for (let sumInput of serviceSums) {
        let sum = parseFloat(sumInput.value) || 0;
        totalCost += sum;
    }

    let totalWithDiscount = totalCost - discount;
    if (totalWithDiscount < 0) totalWithDiscount = 0;

    document.getElementById('total_cost').value = totalCost.toFixed(2);
    document.getElementById('discounted_cost').value = totalWithDiscount.toFixed(2);
}

// Обновляем итоговую стоимость при изменении полей
window.onload = function () {
    // Обработчики для всех новых элементов
    const serviceInputs = document.querySelectorAll('.service-price, .service-quantity, .service-sum');
    for (let input of serviceInputs) {
        input.addEventListener('input', updateTotals);
    }

    const discountInput = document.getElementById('discount');
    if (discountInput) {
        discountInput.addEventListener('input', updateTotals);
    }
};
