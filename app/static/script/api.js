// Эмуляция данных для GET запроса
const mockGetData = [
    { "acceptance_date": "None", "address": "клх Грозный, ул. Крупской, д. 318 к. 46, 764680", "amount": "None", 'client': ' ', "created_at": "2025-01-16T23:36:09.884078", "description": "периферия теряет соединение — мышь или клавиатура иногда теряют связь с компьютером.", "id": "1", "number": "+7 (111) 111-11-11", "performer": "Иван Иванович", "photo_document_back": "None", "photo_document_face": "None", "photo_receipt": "None", "recommendations": "None", "scan_document_back": "None", "scan_document_face": "None", "scan_receipt": "None", "status": "worked"},
    { "acceptance_date": "None", "address": "г. Лодейное Поле, бул. Литейный, д. 7/4 к. 8, 959764", "amount": "None", 'client': 'Синклитикия Альбертовна Александрова', "created_at": "2025-01-12T11:36:09.884078", "description": "не работает клавиатура — она не реагирует на нажатие клавиш, возможно, залипла.", "id": "2", "number": "+7 (222) 222-22-22", "performer": "Петр Петров", "photo_document_back": "None", "photo_document_face": "None", "photo_receipt": "None", "recommendations": "None", "scan_document_back": "None", "scan_document_face": "None", "scan_receipt": "None", "status": "active"}
    // добавьте больше объектов, если нужно
];

// Эмуляция данных для POST запроса
const mockPostData = { 
    "acceptance_date": "None", 
    "address": "г. Лодейное Поле, бул. Литейный, д. 7/4 к. 8, 959764", 
    "amount": "None",
    'client': 'Синклитикия Альбертовна Александрова', 
    "created_at": "2025-01-12T11:36:09.884078", 
    "description": "не работает клавиатура — она не реагирует на нажатие клавиш, возможно, залипла.", 
    "id": "2", 
    "number": "+7 (222) 222-22-22", 
    "performer": "Петр Петров", 
    "photo_document_back": "None", 
    "photo_document_face": "None", 
    "photo_receipt": "None", 
    "recommendations": "None", 
    "scan_document_back": "None", 
    "scan_document_face": "None",
    "scan_receipt": "None", 
    "status": "active"
};

// Функция для выполнения GET запроса (с подделкой данных)
document.getElementById('getRequestBtn').addEventListener('click', function() {
    const responseData = mockGetData;
    document.getElementById('getResponse').innerHTML = `<pre>${JSON.stringify(responseData, null, 2)}</pre>`;
    document.getElementById('getHideBtn').classList.remove('hidden');
});

// Функция для выполнения POST запроса (с подделкой данных)
document.getElementById('postRequestBtn').addEventListener('click', function() {
    const responseData = mockPostData;
    document.getElementById('postResponse').innerHTML = `<pre>${JSON.stringify(responseData, null, 2)}</pre>`;
    document.getElementById('postHideBtn').classList.remove('hidden');
});

// Функция для скрытия ответа GET запроса
document.getElementById('getHideBtn').addEventListener('click', function() {
    document.getElementById('getResponse').innerHTML = '';
    document.getElementById('getHideBtn').classList.add('hidden');
});

// Функция для скрытия ответа POST запроса
document.getElementById('postHideBtn').addEventListener('click', function() {
    document.getElementById('postResponse').innerHTML = '';
    document.getElementById('postHideBtn').classList.add('hidden');
});
