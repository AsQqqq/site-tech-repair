const navigation = document.querySelector('.navigation');
const headerContainer = document.querySelector('.header-container');

document.getElementById('menuToggle').addEventListener('click', function() {
    var navMenu = document.getElementById('navMenu');
    navMenu.classList.toggle('open');
    headerContainer.classList.toggle('menu-open');
});

document.getElementById('closeMenu').addEventListener('click', function() {
    var navMenu = document.getElementById('navMenu');
    navMenu.classList.remove('open');
    headerContainer.classList.toggle('menu-open');
});

document.querySelectorAll('a[active="true"]').forEach(function(link) {
    link.addEventListener('click', function(event) {
        event.preventDefault();  // Останавливаем выполнение действия
        event.stopPropagation();  // Останавливаем распространение события
    });
});
