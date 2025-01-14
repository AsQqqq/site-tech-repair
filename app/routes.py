from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db, login_manager
from app.forms import LoginForm
from werkzeug.utils import secure_filename
from app.models import User, Contract, Service
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import datetime, os



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def is_admin():
    return current_user.is_authenticated and current_user.is_active and int(current_user.level) >= 10

def get_admin_header():
    if is_admin():
        menu_items = [
            {'url': '/new-expense', 'label': 'Новый расход', 'page': 'new-expense'},
            {'url': '/weekly-results', 'label': 'Итоги недели', 'page': 'weekly-results'},
            {'url': '/application-admin', 'label': 'Заявки на проверке', 'page': 'application-admin'},
        ]
        return menu_items
    return []

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Вход успешен', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template(
        'login.html', 
        form=form
    )


@app.route('/admin')
@login_required
def admin():
    applications = Contract.query.filter(Contract.status == "active").all()

    username = current_user.first_name
    active_application = current_user.active_applications
    return render_template('main.html', 
        applications=applications, 
        active_application=active_application,
        menu_items=get_admin_header(), 
        active_page='home', 
        profile_name=username
    )


@app.route('/applications')
@login_required
def applications():
    applications = Contract.query.all()
    
    username = current_user.first_name
    active_application = current_user.active_applications
    
    # Передаем данные в шаблон
    return render_template('applications.html', 
                           menu_items=get_admin_header(), 
                           active_application=active_application,
                           active_page='applications', 
                           profile_name=username,
                           applications=applications)


@app.route('/finance')
@login_required
def finance():
    income = 50000
    expense = 10000
    result = income - expense

    historys = [
        {
            "id": "001",
            "date": "Date for expense #001",
            "description": "Description for expense #001",
            "amount": "500",
            "type": "Доход"
        },
        {
            "id": "002",
            "date": "Date for expense #002",
            "description": "Description for expense #002",
            "amount": "55000",
            "type": "Доход"
        },
        {
            "id": "003",
            "date": "Date for expense #003",
            "description": "Description for expense #003",
            "amount": "3000",
            "type": "Расход"
        },
        {
            "id": "004",
            "date": "Date for expense #004",
            "description": "Description for expense #004",
            "amount": "1000",
            "type": "Доход"
        },
    ]
    username = current_user.first_name
    active_application = current_user.active_applications
    return render_template('finance.html', 
        menu_items=get_admin_header(), 
        active_application=active_application,
        income=income, 
        expense=expense, 
        result=result, 
        historys=historys, 
        active_page='finance', 
        profile_name=username
    )
                           

@app.route('/new-expense')
@login_required
def new_expense():
    if is_admin():
        username = current_user.first_name
        active_application = current_user.active_applications
        return render_template('newExpense.html', 
            menu_items=get_admin_header(), 
            active_application=active_application,
            active_page='new-expense', 
            profile_name=username
        )


@app.route('/new-application', methods=['GET', 'POST'])
@login_required
def new_application():
    if request.method == 'POST':
        description = request.form.get('expenseDescription')
        address = request.form.get('expenseTitle')
        client = request.form.get('expenseClient')
        number = request.form.get('expenseNumber')
        performer = f"{current_user.first_name} {current_user.last_name}"

        new_contract = Contract(
            description=description,
            address=address,
            client=client,
            number=number,
            performer=performer
        )
        db.session.add(new_contract)
        db.session.commit()
        
        return redirect(url_for('applications'))
    username = current_user.first_name
    active_application = current_user.active_applications
    return render_template('newApplication.html', 
        menu_items=get_admin_header(), 
        active_application=active_application,
        profile_name=username
    )


# Проверка расширения файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/end-application', methods=['POST'])
@login_required
def end_application():
    expenseId = request.form.get('expenseId')
    
    if int(current_user.active_applications) == int(expenseId):
        # Получаем данные из формы
        expenseCreatedAt = request.form.get('expenseCreatedAt')
        expenseDescription = request.form.get('expenseDescription')
        expenseClient = request.form.get('expenseClient')
        expenseAddress = request.form.get('expenseAddress')
        expenseAmount = request.form.get('expenseAmount')
        expenseRecommendation = request.form.get('expenseRecommendation')
        expensePerformer = request.form.get('expensePerformer')
        expenseAcceotanceDate = request.form.get('expenseAcceotanceDate')

        # Получаем данные об услугах
        serviceNames = request.form.getlist('serviceName[]')
        servicePrices = request.form.getlist('servicePrice[]')
        serviceQuantities = request.form.getlist('serviceQuantity[]')
        serviceTotals = request.form.getlist('serviceTotal[]')
        serviceWarranties = request.form.getlist('serviceWarranty[]')

        # Проверка обязательных полей для заявки
        missing_fields = []

        if not expenseCreatedAt:
            missing_fields.append('Дата подачи заявки')
        if not expenseDescription:
            missing_fields.append('Описание')
        if not expenseClient:
            missing_fields.append('Клиент')
        if not expenseAddress:
            missing_fields.append('Адрес')
        if not expenseAmount:
            missing_fields.append('Сумма')
        if not expenseRecommendation:
            missing_fields.append('Рекомендации')
        if not expensePerformer:
            missing_fields.append('Исполнитель')
        if not expenseAcceotanceDate:
            missing_fields.append('Дата исполнения')

        # Проверка полей об услугах
        for i, name in enumerate(serviceNames):
            if not name or not servicePrices[i] or not serviceQuantities[i] or not serviceTotals[i]:
                missing_fields.append(f"Услуга {i+1} не заполнена корректно")

        # Определяем словарь с ключами для фотографий и их колонками в базе данных
        photos = {
            'photo1': 'photo_receipt',
            'photo2': 'photo_document_face',
            'photo3': 'photo_document_back'
        }

        photo_paths = {}  # Используем словарь для хранения путей к фото

        # Проверяем, что все три фото загружены и валидны
        for photo_key, column_name in photos.items():
            photo = request.files.get(photo_key)
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(filepath)
                photo_paths[column_name] = filepath  # Сохраняем путь к фото в словарь
            else:
                # Если хотя бы одно фото не загружено или не валидное
                missing_fields.append(f'{column_name} должно быть загружено и иметь допустимый формат.')

        # Если не загружены все три фотки
        if len(photo_paths) != 3:
            missing_fields.append('Пожалуйста, загрузите все три фотографии: чек, лицевая и задняя сторона документа.')

        # Если есть ошибки, возвращаем пользователя на форму
        if missing_fields:
            flash(f"Пожалуйста, заполните следующие поля: {', '.join(missing_fields)}", 'error')
            return redirect(url_for('end_application', id=expenseId))

        acceotance_date = datetime.datetime.now()

        # Сохраняем данные в базу данных
        application = Contract.query.filter_by(id=int(expenseId)).first()
        application.status = 'checked'
        application.amount = expenseAmount
        application.acceptance_date = acceotance_date
        application.recommendations = expenseRecommendation
        if application.client != expenseClient:
            application.client = expenseClient

        # Обновляем пути к фотографиям из словаря
        application.photo_receipt = photo_paths.get('photo_receipt')
        application.photo_document_face = photo_paths.get('photo_document_face')
        application.photo_document_back = photo_paths.get('photo_document_back')

        db.session.commit()

        # Обработка услуг
        for i in range(len(serviceNames)):
            service_name = serviceNames[i]
            service_price = float(servicePrices[i]) if servicePrices[i] else 0.0
            service_quantity = int(serviceQuantities[i]) if serviceQuantities[i] else 0
            service_total = float(serviceTotals[i]) if serviceTotals[i] else 0.0
            service_warranty = serviceWarranties[i]

            service = Service(
                contract_id=expenseId,
                name=service_name,
                price=service_price,
                quantity=service_quantity,
                sum=service_total,
                warranty=service_warranty
            )
            
            db.session.add(service)
        
        db.session.commit()

        # Снимаем активную заявку с пользователя
        current_user.active_applications = None
        db.session.commit()

        # Успешно завершено, перенаправляем
        flash('Заявка успешно завершена.', 'success')
        return redirect(url_for('applications'))
    else:
        flash("Вы не можете завершить эту заявку.", 'error')
        return redirect(url_for('applications'))



@app.route('/flash-message', methods=['POST'])
def flash_message():
    message = request.form.get('message')
    if message:
        flash(message, 'danger')
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error'}), 400


@app.route('/edit-<id>-application')
@login_required
def edit_application(id):
    id_application = f"#{id}"
    description = "Description for application #" + id
    address = "Address for application #" + id
    client = "Client for application #" + id

    username = current_user.first_name
    active_application = current_user.active_applications
    return render_template(
        'newEditReadApplications.html', 
        menu_items=get_admin_header(),
        id_application=id_application,
        active_application=active_application,
        description=description, 
        address=address, 
        client=client, 
        profile_name=username
    )


@app.route('/<id>-application')
@login_required
def read_application(id):
    application = Contract.query.filter(Contract.id == id).first()

    if application.status.value == "closed" or application.status.value == "checked":
        id_application = int(id)
        created_at = application.created_at
        acceptance_date = application.acceptance_date.strftime("%Y-%m-%d %H:%M:%S")
        client = application.client
        description = application.description
        address = application.address
        number = application.number
        recommendation = application.recommendations
        performer = application.performer
        amount = application.amount

        photo1_db = application.photo_receipt
        photo2_db = application.photo_document_face
        photo3_db = application.photo_document_back

        photo1 = str(photo1_db).replace("app/", "").replace("\\", "/")
        photo2 = str(photo2_db).replace("app/", "").replace("\\", "/")
        photo3 = str(photo3_db).replace("app/", "").replace("\\", "/")

        username = current_user.first_name
        active_application = current_user.active_applications

        return render_template('readFinishApplication.html', 
            id_application=id_application,
            created_at=created_at,
            acceptance_date=acceptance_date,
            status=application.status.value,
            client=client,
            description=description,
            address=address,
            number=number,
            recommendation=recommendation,
            performer=performer,
            amount=amount,
            active_application=active_application,
            photo1=photo1,
            photo2=photo2,
            photo3=photo3,
            profile_name=username,
            active_page='application',
            menu_items=get_admin_header(),
        )

    
    id_application = int(id)
    description = application.description
    address = application.address
    client = application.client
    number = application.number
    status = False if application.status.value == "closed" else True

    if current_user.active_applications == int(id):
        worked_application = True
    else:
        worked_application = False


    username = current_user.first_name
    active_application = current_user.active_applications
    checked = True if application.status.value == "checked" else False
    return render_template('readApplication.html', 
        active=status,
        worked=worked_application,
        checked=checked,
        active_application=active_application,
        closed=True if application.status.value == "closed" else False,
        menu_items=get_admin_header(),
        id_application=id_application,
        description=description,
        date = application.created_at,
        address=address, 
        client=client,
        number=number,
        profile_name=username,
        active_page='application'
    )


@app.route('/end-application-<int:id>')
@login_required
def end_application_id(id):
    if current_user.active_applications == id:
        application = Contract.query.filter(Contract.id == id).first()

        created_at = application.created_at
        address = application.address
        client = application.client
        description = application.description
        performer = application.performer
        acceotance_date_pre = datetime.datetime.now()
        acceotance_date = acceotance_date_pre.strftime('%Y-%m-%d %H:%M')


        username = current_user.first_name
        active_application = current_user.active_applications
        return render_template('endApplication.html', 
            menu_items=get_admin_header(),
            id=id,
            created_at=created_at,
            address=address,
            client=client,
            active_application=active_application,
            description=description,
            performer=performer,
            acceotance_date=acceotance_date,
            profile_name=username
        )
    return redirect(url_for('applications'))


@app.route('/delete_application/<int:id>', methods=['POST'])
@login_required
def delete_application(id):
    application = Contract.query.filter_by(id=id).first()

    if application:
        try:
            db.session.delete(application)
            db.session.commit()
            flash('Заявка успешно удалена!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении заявки.', 'danger')
    else:
        flash('Заявка не найдена.', 'danger')

    return redirect(url_for('applications'))


@app.route('/apply_application/<int:id>', methods=['POST'])
@login_required
def apply_application(id):
    application = Contract.query.filter_by(id=id).first()

    if current_user.active_applications:
        flash('Вы уже в заявке.', 'danger')
        return redirect(url_for('admin'))

    if application:
        try:
            # Изменяем статус заявки на 'worked'
            application.status = 'worked'
            db.session.commit()
            current_user.active_applications = id
            db.session.commit()
            flash('Заявка успешно принята!', 'success')  # Выводим сообщение об успешном принятии заяв
        except Exception as e:
            db.session.rollback()  # В случае ошибки откатываем изменения
            flash('Ошибка при принятии заявки.', 'danger')  # Выводим сообщение об ошибке при принятии заявки
    else:
        flash('Заявка не найдена.', 'danger')  # Выводим сообщение об отсутствии заявки

    return redirect(url_for('admin'))



@app.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно вышли', 'success')
    return redirect(url_for('login'))
