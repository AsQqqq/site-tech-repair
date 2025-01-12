from flask import render_template, flash, redirect, url_for, request
from app import app, db, login_manager
from app.forms import LoginForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


def is_admin():
    return current_user.is_authenticated and current_user.is_active and int(current_user.level) >= 10

def get_admin_header():
    if is_admin():
        menu_items = [
            {'url': '/new-expense', 'label': 'Новый расход', 'page': 'new-expense'},
            {'url': '/weekly-results', 'label': 'Итоги недели', 'page': 'weekly-results'}
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
        
        # Пытаемся найти пользователя по имени
        user = User.query.filter_by(username=username).first()
        
        # Если пользователь найден и пароль верный
        if user and check_password_hash(user.password_hash, password):
            login_user(user)  # Входим в систему
            flash('Вход успешен', 'success')
            return redirect(url_for('admin'))  # Перенаправляем на главную страницу
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('login.html', form=form)


@app.route('/admin')
@login_required
def admin():
    applications = [
        {
            "id": "001",
            "description": "Description for application #001",
            "address": "Address for application #001",
            "url": "/001-application"
        },
        {
            "id": "002",
            "description": "Description for application #002",
            "address": "Address for application #002",
            "url": "/002-application"
        },
        {
            "id": "003",
            "description": "Description for application #003",
            "address": "Address for application #003",
            "url": "/003-application"
        },
        {
            "id": "004",
            "description": "Description for application #004",
            "address": "Address for application #004",
            "url": "/004-application"
        },
        {
            "id": "005",
            "description": "Description for application #005",
            "address": "Address for application #005",
            "url": "/005-application"
        },
    ]
    username = current_user.first_name
    return render_template('main.html', applications=applications, menu_items=get_admin_header(), active_page='home', profile_name=username)


@app.route('/applications')
@login_required
def applications():
    username = current_user.first_name
    return render_template('applications.html', menu_items=get_admin_header(), active_page='applications', profile_name=username)


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
    return render_template('finance.html', menu_items=get_admin_header(), income=income, expense=expense, result=result, historys=historys, active_page='finance', profile_name=username)
                           

@app.route('/new-expense')
@login_required
def new_expense():
    if is_admin():
        username = current_user.first_name
        return render_template('newExpense.html', menu_items=get_admin_header(), active_page='new-expense', profile_name=username)


@app.route('/new-application', methods=['GET', 'POST'])
@login_required
def new_application():
    if request.method == 'POST':
        description = request.form.get('expenseDescription')
        address = request.form.get('expenseTitle')
        client = request.form.get('expenseClient')

        print(f"Описание: {description}, Адрес: {address}, Клиент: {client}")
        
        return redirect(url_for('applications'))
    username = current_user.first_name
    return render_template('newEditReadApplications.html', new=True, menu_items=get_admin_header(), profile_name=username)


@app.route('/edit-<id>-application')
@login_required
def edit_application(id):
    id_application = f"#{id}"
    description = "Description for application #" + id
    address = "Address for application #" + id
    client = "Client for application #" + id

    username = current_user.first_name
    return render_template('newEditReadApplications.html', new=False, menu_items=get_admin_header(), id_application=id_application, description=description, address=address, client=client, profile_name=username)


@app.route('/<id>-application')
@login_required
def read_application(id):
    id_application = f"#{id}"
    description = "Description for application #" + id
    address = "Address for application #" + id
    client = "Client for application #" + id

    username = current_user.first_name
    return render_template('newEditReadApplications.html', new=False, read=True, active=True, menu_items=get_admin_header(), id_application=id_application, description=description, address=address, client=client, profile_name=username)
    

@app.route('/logout')
def logout():
    logout_user()  # Завершаем сессию текущего пользователя
    flash('Вы успешно вышли', 'success')  # Сообщение о выходе
    return redirect(url_for('login'))  # Перенаправление на страницу входа
