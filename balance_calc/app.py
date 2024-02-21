import os
import random
from flask_caching import Cache
from dotenv import load_dotenv
from flask import Flask, request, render_template, flash, get_flashed_messages
from balance_calc.utility import fetch_weather
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})

app = Flask(__name__)
cache.init_app(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)


class User(db.Model):
    """
    Создание модели User и методов для работы с объектом класса.
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def create(self, useranme, balance):
        """Создание пользователя"""
        self.username = useranme
        self.balance = balance
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Удалене пользователя"""
        db.session.delete(self)
        db.session.commit()

    def update_username(self, username):
        """Обновление username пользователя"""
        self.username = username
        db.session.commit()

    def update_balance(self, balance):
        """Обновление баланса пользователя"""
        self.balance = balance
        db.session.commit()

    def __repr__(self):
        return "<UserModel %r>" % self.id


with app.app_context():
    """
    Создание экземпляра базы данных и таблиц, если еще не созданы. 
    Создание 5 пользователей с балансами, если таблица 
    users пустая.    
    """
    db.create_all()
    if User().query.count() == 0:
        for i in range(1, 6):
            username = f"username{i}"
            balance = random.randint(5000, 15000)
            User().create(useranme=username, balance=balance)


@app.route('/')
def index():
    """Стартовая страница"""
    return ("Для изменения баланса перейдите на "
            "http://0.0.0.0:8000/update/balance или "
            "http://127.0.0.1:5000/update/balance, "
            "в зависимости от режима работы")


@app.route('/update/balance', methods=["POST", "GET"])
def update_balance():
    if request.method == "POST":
        """Получение id юзера и города"""
        user_id = request.form["user_id"]
        city = request.form["city"]
        """
        Проверка наличия в кэше данных по городу. Если города в кэше нет, то 
        добавляем.
        """
        if not cache.get(city):
            city_datas = fetch_weather(city)
            city_temp = city_datas["city_temp"]
            cache.set(city, city_temp, timeout=600)
        else:
            city_temp = cache.get(city)

        user = None
        if user_id:
            """Дополнительная проверка, что id получен"""
            user = User.query.get(ident=user_id)

        if user:
            """
            Проверка, что юзер по id есть в базе. Если да, то расчет нового баланса
            Если новый баланс больше ноля, то обновляем его значение в базе. Если нет, 
            то баланс приравнивается к нолю.
            """
            new_balance = user.balance + city_temp
            if new_balance > 0:
                user.update_balance(balance=user.balance+city_temp)
            else:
                user.update_balance(balance=0)
            return render_template('update_balance.html')
        else:
            flash("Пользователя с таким id не существует")
            messages = get_flashed_messages()
            return render_template('update_balance.html', messages=messages)
    else:
        return render_template('update_balance.html')
