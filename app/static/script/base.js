// Обработчик события для кнопки "Вернуться"
document.getElementById('back').addEventListener('click', function() {
    window.history.back(); // Возвращаемся на предыдущую страницу
});

// Получаем элементы модального окна и кнопки
const confirmationModal = document.getElementById('confirmationModal');
const confirmDelete = document.getElementById('confirmDelete');
const cancelDelete = document.getElementById('cancelDelete');
const cancelButton = document.getElementById('cansel');
const expenseForm = document.querySelector('#expenseForm');

// Показать модальное окно при нажатии на кнопку "Отменить заявку"
cancelButton.addEventListener('click', function(event) {
    event.preventDefault(); // Отменить стандартное действие
    confirmationModal.style.display = 'block'; // Показать модальное окно
});

// Закрыть модальное окно при нажатии на "Нет, вернуть"
cancelDelete.addEventListener('click', function() {
    confirmationModal.style.display = 'none'; // Закрыть модальное окно
});

// Отправить форму при нажатии на "Да, отменить"
confirmDelete.addEventListener('click', function() {
    expenseForm.submit(); // Отправить форму
});