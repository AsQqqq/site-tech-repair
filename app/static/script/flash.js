// Обработчик для закрытия flash-сообщений по клику на крестик
document.addEventListener('DOMContentLoaded', function () {
    var flashMessages = document.querySelectorAll('.flash-message');
    
    // Для каждого flash-сообщения добавляем функциональность для закрытия
    flashMessages.forEach(function (message) {
        var closeBtn = message.querySelector('.flash-message-close');
        
        // Закрытие при клике на крестик
        closeBtn.addEventListener('click', function () {
            message.style.opacity = 0;
            setTimeout(function () {
                message.style.display = 'none';
            }, 500);
        });

        // Плавное исчезновение через 3 секунды
        setTimeout(function () {
            message.style.opacity = 0;
            setTimeout(function () {
                message.style.display = 'none';
            }, 500);
        }, 15000); // 15000ms = 15 секунды
    });
});

// После того как сообщения будут загружены, показываем их с анимацией
document.addEventListener('DOMContentLoaded', function () {
    var flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function (message) {
        message.style.display = 'block';
        setTimeout(function () {
            message.style.opacity = 1;
        }, 10); // Небольшая задержка, чтобы увидеть анимацию
    });
});
