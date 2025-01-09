import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
from docx import Document
from datetime import datetime

app = Flask(__name__)

# Секретный ключ для работы с сессиями
app.secret_key = os.urandom(24)

# Папка для загрузки файлов
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Пароль для входа
ADMIN_PASSWORD = 'h5wwLy'  # Лучше хранить в переменных окружения

# Функция для создания папки с номером заявки
def create_directory_for_order(order_number):
    order_dir = os.path.join(app.config['UPLOAD_FOLDER'], order_number)
    if not os.path.exists(order_dir):
        os.makedirs(order_dir)
    return order_dir

# Проверка аутентификации
def is_authenticated():
    return 'authenticated' in session and session['authenticated']

# Главная страница
@app.route('/')
def index():
    orders = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', orders=orders)

# Страница входа (admin)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if is_authenticated():
        return redirect(url_for('main'))  # Переход на страницу загрузки при авторизации

    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('main'))  # Переход на страницу загрузки при успешном входе
        else:
            return "Неверный пароль. Попробуйте снова."

    return render_template('admin_login.html')


@app.route('/main', methods=['GET', 'POST'])
def main():

    if not is_authenticated():
        return redirect(url_for('admin'))
    
    search_query = request.args.get('search', '').lower()  # Получаем запрос из формы поиска
    
    # Получаем список всех заявок
    orders = os.listdir(UPLOAD_FOLDER)
    
    filtered_orders = []

    # Если есть запрос для поиска, фильтруем список заявок
    for order in orders:
        order_dir = os.path.join(app.config['UPLOAD_FOLDER'], order)
        
        # Проверяем только если папка существует и содержит файлы
        if os.path.isdir(order_dir):
            # Ищем в DOCX файле с информацией о заявке
            doc_file_path = None
            for file_ in os.listdir(order_dir):
                if file_.endswith('.docx'):
                    doc_file_path = os.path.join(order_dir, file_)
                    break
            
            if doc_file_path:
                doc = Document(doc_file_path)
                text_content = ' '.join([para.text.lower() for para in doc.paragraphs])  # Собираем все тексты из документа в одну строку
                
                # Если в тексте документа встречается поисковый запрос, добавляем заявку в результаты
                if search_query in text_content:
                    filtered_orders.append(order)

    # Если не было найдено совпадений по запросу, показываем все заявки
    if search_query:
        orders = filtered_orders

    # Возвращаем шаблон с отфильтрованными заявками
    return render_template('admin_index.html', orders=orders)



# Страница загрузки заявки (upload)
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not is_authenticated():
        return redirect(url_for('admin'))  # Если не авторизован, перенаправление на страницу логина

    if request.method == 'POST':
        # Получение данных из формы
        name = request.form['name']
        address = request.form['address']
        services = request.form.getlist('services[]')  # Список услуг
        prices = request.form.getlist('prices[]')  # Список цен
        quantities = request.form.getlist('quantities[]')  # Список количеств
        sums = request.form.getlist('sums[]')  # Список сумм
        warranties = request.form.getlist('warranties[]')  # Список гарантий
        discount = float(request.form['discount'])  # Скидка
        total_cost = float(request.form['total_cost'])  # Стоимость услуг
        discounted_cost = float(request.form['discounted_cost'])  # Сумма к оплате
        recommendations = request.form['recommendations']
        order_number = request.form['order_number']  # Номер заявки
        order_date_str = request.form['order_date']  # Дата заявки

        # Преобразуем строку с датой в объект datetime
        try:
            order_date = datetime.strptime(order_date_str, "%d.%m.%Y")
        except ValueError:
            return "Ошибка: Неверный формат даты. Используйте формат: ДД.ММ.ГГГГ"

        # Получение файлов
        receipt_file = request.files['receipt']
        document_file1 = request.files['document1']
        document_file2 = request.files['document2']

        # Создание папки для заявок
        order_dir = create_directory_for_order(order_number)

        # Генерация новых имен файлов на английском языке
        receipt_filename = 'receipt.jpg'  # Переименование в чек
        document_filename1 = 'document1.jpg'  # Переименование в документ 1
        document_filename2 = 'document2.jpg'  # Переименование в документ 2

        # Путь к сохранению файлов
        receipt_path = os.path.join(order_dir, receipt_filename)
        document_path1 = os.path.join(order_dir, document_filename1)
        document_path2 = os.path.join(order_dir, document_filename2)

        # Сохранение файлов
        receipt_file.save(receipt_path)
        document_file1.save(document_path1)
        document_file2.save(document_path2)

        # Генерация DOCX документа
        doc = Document()
        doc.add_heading('Документ о выполненных работах', 0)

        doc.add_paragraph(f'Исполнитель: {name}')
        doc.add_paragraph(f'Адрес выполнения работ: {address}')
        doc.add_paragraph(f'Рекомендации: {recommendations}')
        doc.add_paragraph(f'Номер заявки: {order_number}')
        doc.add_paragraph(f'Дата выполнения работ: {order_date.strftime("%Y-%m-%d")}')

        # Добавляем информацию о услугах
        for i in range(len(services)):
            doc.add_paragraph(f'Услуга: {services[i]}')
            doc.add_paragraph(f'Цена: {prices[i]}')
            doc.add_paragraph(f'Количество: {quantities[i]}')
            doc.add_paragraph(f'Сумма: {sums[i]}')
            doc.add_paragraph(f'Гарантия: {warranties[i]}')

        # Добавляем стоимость услуг и скидку
        doc.add_paragraph(f'Стоимость услуг: {total_cost}')
        doc.add_paragraph(f'Скидка: {discount}')
        doc.add_paragraph(f'К оплате: {discounted_cost}')

        # Вставляем ссылки на файлы (новые имена)
        doc.add_paragraph(f'Чек: {receipt_filename}')
        doc.add_paragraph(f'Документ (сторона 1): {document_filename1}')
        doc.add_paragraph(f'Документ (сторона 2): {document_filename2}')

        # Сохранение документа
        doc_filename = f'{order_number}_document.docx'
        doc_path = os.path.join(order_dir, doc_filename)
        doc.save(doc_path)

        # Перенаправляем на главную страницу
        return redirect(url_for('main'))

    return render_template('upload.html')





# Добавляем маршрут для обработки статических файлов
@app.route('/uploads/<order_number>/<filename>')
def uploaded_file(order_number, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], order_number), filename)


@app.route('/view_order/<order_number>', methods=['GET'])
def view_order(order_number):
    if not is_authenticated():
        return redirect(url_for('admin'))
    
    # Путь к папке с заказом в директории 'uploads'
    order_dir = os.path.join('uploads', order_number)  # Папка с заказом внутри uploads
    if not os.path.exists(order_dir):
        return "Заказ не найден", 404

    # Путь к DOCX документу
    doc_filename = f'{order_number}_document.docx'
    doc_path = os.path.join(order_dir, doc_filename)
    
    if not os.path.exists(doc_path):
        return "Документ не найден", 404

    # Открытие и чтение документа
    doc = Document(doc_path)

    order_data = {}
    order_data['services'] = []

    for para in doc.paragraphs:
        text = para.text.strip()  # Убираем лишние пробелы

        if text.startswith('Исполнитель:'):
            order_data['name'] = text.replace('Исполнитель:', '').strip()
        elif text.startswith('Адрес выполнения работ:'):
            order_data['address'] = text.replace('Адрес выполнения работ:', '').strip()
        elif text.startswith('Рекомендации:'):
            order_data['recommendations'] = text.replace('Рекомендации:', '').strip()
        elif text.startswith('Номер заявки:'):
            order_data['order_number'] = text.replace('Номер заявки:', '').strip()
        elif text.startswith('Дата выполнения работ:'):
            order_data['order_date'] = text.replace('Дата выполнения работ:', '').strip()
        elif text.startswith('Стоимость услуг:'):
            order_data['total_cost'] = text.replace('Стоимость услуг:', '').strip()
        elif text.startswith('Скидка:'):
            order_data['discount'] = text.replace('Скидка:', '').strip()
        elif text.startswith('К оплате:'):
            order_data['discounted_cost'] = text.replace('К оплате:', '').strip()
        elif text.startswith('Чек:'):
            order_data['receipt_filename'] = text.replace('Чек:', '').strip()
        elif text.startswith('Документ (сторона 1):'):
            order_data['document_filename1'] = text.replace('Документ (сторона 1):', '').strip()
        elif text.startswith('Документ (сторона 2):'):
            order_data['document_filename2'] = text.replace('Документ (сторона 2):', '').strip()
        elif text.startswith('Услуга:'):
            service = {}
            service['name'] = text.replace('Услуга:', '').strip()
            order_data['services'].append(service)
        elif text.startswith('Цена:') and order_data['services']:
            order_data['services'][-1]['price'] = text.replace('Цена:', '').strip()
        elif text.startswith('Количество:') and order_data['services']:
            order_data['services'][-1]['quantity'] = text.replace('Количество:', '').strip()
        elif text.startswith('Сумма:') and order_data['services']:
            order_data['services'][-1]['sum'] = text.replace('Сумма:', '').strip()
        elif text.startswith('Гарантия:') and order_data['services']:
            order_data['services'][-1]['warranty'] = text.replace('Гарантия:', '').strip()
        

    # Формируем URL-адреса для файлов
    receipt_url = url_for('static', filename=f'uploads/{order_number}/{order_data["receipt_filename"]}')
    document_url1 = url_for('static', filename=f'uploads/{order_number}/{order_data["document_filename1"]}')
    document_url2 = url_for('static', filename=f'uploads/{order_number}/{order_data["document_filename2"]}')


    # Возвращаем информацию на страницу
    return render_template('view_order.html',
            order_data=order_data, 
            receipt_url=receipt_url,
            document_url1=document_url1,
            document_url2=document_url2
    )



# Выход из системы
@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
