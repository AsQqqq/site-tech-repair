document.getElementById('menuToggle').addEventListener('click', function() {
    var navMenu = document.getElementById('navMenu');
    navMenu.classList.toggle('open');
});

document.getElementById('closeMenu').addEventListener('click', function() {
    var navMenu = document.getElementById('navMenu');
    navMenu.classList.remove('open');
});

document.querySelectorAll('a[active="true"]').forEach(function(link) {
    link.addEventListener('click', function(event) {
        event.preventDefault();  // Останавливаем выполнение действия
        event.stopPropagation();  // Останавливаем распространение события
    });
});
