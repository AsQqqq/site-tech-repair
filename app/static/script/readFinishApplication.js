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