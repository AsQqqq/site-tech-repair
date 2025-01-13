document.addEventListener('DOMContentLoaded', function() {
    const addressElement = document.querySelector('.address');
    const maxLength = 30;
  
    // Если текст слишком длинный, обрезаем и добавляем многоточие
    if (addressElement.textContent.length > maxLength) {
      addressElement.textContent = addressElement.textContent.substring(0, maxLength) + '...';
    }
  });
  

  document.addEventListener('DOMContentLoaded', function() {
    const descriptionElement = document.querySelector('.description');
    const maxLength = 30;
  
    // Если текст слишком длинный, обрезаем и добавляем многоточие
    if (descriptionElement.textContent.length > maxLength) {
      descriptionElement.textContent = descriptionElement.textContent.substring(0, maxLength) + '...';
    }
  });
  