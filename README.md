## Установка  
git clone git@github.com:TarakanovAndrey/test_project.git  
make install  
В директории проекта создайте файл .env и задайте перменные окружения:  
SECRET_KEY= -любая длинная последовательность различных символов.  
OPENWEATHERMAP_KEY= - получаете при создании аккаунта на https://openweathermap.org/  
SQLALCHEMY_DATABASE_URI=sqlite:///db.db

## Запуск  
make start  

## Описание  
1. Основной функционал реализован в файле app.py. При увелчении функционала необходимо 
разбить на модули.
2. Получение температуры реализована в utility.py(fetch_weather(city)). На вход подается название города на 
латиннице. Функция ищет первое полное совпадение и получает температуру этого города. Использовано открытое API 
https://openweathermap.org/. Правильнее подавать на вход функции id для конкретного города, так как по названию 
может выводиться несколько результатов. 
3. При создании приложения автоматически создается пять пользователей с балансами от 5000 до 15000. Они создаются, если 
проверка показывает, что таблица пустая.
4. Если температура города уже запрашивалась, то ее значение сохраняется в кэше сервера и хранится там в течении 600 
секунд.
5. Баланс увеличивается или уменьшается в зависмости от знака температуры. Если итоговое значение баланса может стать 
меньше ноля, то баланс приравнивается к нолю.
6. Gunicorn запускается по схеме процессы + gevent командой make start. Для запуска dev сервера исполльзуется команда 
команда make dev.
7. Обновление баланса происходит по url "http://127.0.0.1:5000/update/balance" - dev режим и 
"http://0.0.0.0:8000/update/balance" - рабочий режим. Реализован шаблон. 