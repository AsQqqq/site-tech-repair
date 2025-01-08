function contactUs() {
    if (window.innerWidth <= 768) {
        // Для мобильных устройств инициируем звонок
        window.location.href = "tel:8915222006";
    } else {
        // Для ПК показываем номер телефона в модальном окне
        document.getElementById('modal').classList.add('show');
    }
}

function closeModal() {
    document.getElementById('modal').classList.remove('show');
}