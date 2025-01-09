// Функция для открытия изображения в модальном окне
function openImage(imageUrl) {
    var modal = document.getElementById('modal');
    var modalImage = document.getElementById('modalImage');
    
    // Устанавливаем источник изображения
    modalImage.src = imageUrl;
    
    // Показываем модальное окно
    modal.style.display = "block";
}

// Функция для закрытия модального окна
function closeModal() {
    var modal = document.getElementById('modal');
    modal.style.display = "none";
}

// Закрыть модальное окно, если кликнуть вне изображения
window.onclick = function(event) {
    var modal = document.getElementById('modal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
