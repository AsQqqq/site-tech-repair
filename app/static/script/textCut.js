document.addEventListener('DOMContentLoaded', function() {
  const maxLength = 30;

  // Для всех элементов с классом 'address'
  const addressElements = document.querySelectorAll('.address');
  addressElements.forEach(function(addressElement) {
      // Если текст слишком длинный, обрезаем и добавляем многоточие
      if (addressElement.textContent.length > maxLength) {
          addressElement.textContent = addressElement.textContent.substring(0, maxLength) + '...';
      }
  });

  // Для всех элементов с классом 'description'
  const descriptionElements = document.querySelectorAll('.description');
  descriptionElements.forEach(function(descriptionElement) {
      // Если текст слишком длинный, обрезаем и добавляем многоточие
      if (descriptionElement.textContent.length > maxLength) {
          descriptionElement.textContent = descriptionElement.textContent.substring(0, maxLength) + '...';
      }
  });
});
