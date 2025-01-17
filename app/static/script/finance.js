function sortTable(columnIndex) {
    var table = document.querySelector('.history-table');
    var rows = Array.from(table.rows).slice(1);  // исключаем заголовок
    var isAscending = table.getAttribute('data-sort-order') === 'asc';

    // Убираем стрелки для всех заголовков
    var headers = table.querySelectorAll('th span .sort-arrow');
    headers.forEach(function(arrow) {
        arrow.style.visibility = 'hidden';
        arrow.classList.remove('asc', 'desc');
    });

    // Добавляем стрелку для выбранного столбца
    var currentArrow = table.rows[0].cells[columnIndex].querySelector('.sort-arrow');
    currentArrow.style.visibility = 'visible';
    currentArrow.classList.add(isAscending ? 'desc' : 'asc');

    // Сортируем строки по выбранной колонке
    rows.sort(function(rowA, rowB) {
        var cellA = rowA.cells[columnIndex].innerText;
        var cellB = rowB.cells[columnIndex].innerText;

        // Преобразуем дату в формат для сравнения, если это колонка "Дата"
        if (columnIndex === 1) {
            cellA = new Date(cellA);
            cellB = new Date(cellB);
        }

        if (cellA < cellB) return isAscending ? -1 : 1;
        if (cellA > cellB) return isAscending ? 1 : -1;
        return 0;
    });

    // Перемещаем отсортированные строки в таблицу
    rows.forEach(function(row) {
        table.appendChild(row);
    });

    // Переключаем направление сортировки для следующего клика
    table.setAttribute('data-sort-order', isAscending ? 'desc' : 'asc');
}