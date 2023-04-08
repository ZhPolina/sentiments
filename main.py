# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import os
from flask_mysqldb import MySQL
import re
import MySQLdb.cursors
from googletrans import Translator
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import fasttext

fasttext.FastText.eprint = lambda x: None

app = Flask(__name__)

translator = Translator()


app.secret_key = os.urandom(24)
'''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
'''
app.config['MYSQL_DB'] = 'flask'
app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_PASSWORD'] = '9156'
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8'

mysql = MySQL(app)
PEOPLE_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

# открытие главной страницы
@app.route('/', methods=['GET'])
def main():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'background_image.jpg')
    return render_template('main.html', background_image = full_filename)

# функция поиска мест досуга по заданному пользователем городу
@app.route('/search_by_city', methods=['POST'])
def search_by_city():
    cursor = mysql.connection.cursor()
    city = request.form['city']  
    cursor.execute('SELECT id_places, name, link, image, description, rating, avg_emotion FROM places WHERE city = %s ORDER by rating DESC', (city, ))
    data = cursor.fetchall()
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'])
    if data:
        return render_template('leisure_venues.html', full_filename = full_filename, data = data, city = city)
    else:
        return render_template('leisure_venues.html', full_filename = full_filename, data = data, message = "Нет результатов по Вашему запросу.", city = city)

# функция вывода всписка мест проведения досуга
@app.route('/leisure_venues', methods=['GET','POST'])
def leisure_venues():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id_places, name, link, image, description, rating, avg_emotion FROM places ORDER by rating DESC')
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'])
    data = cursor.fetchall()
    cursor.close()
    return render_template('leisure_venues.html', full_filename = full_filename, data = data)

# функция входа в систему
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    value = "Вход"
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        value = "Вход"
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            value = "Выход"
            return render_template('home_page.html', msg = msg, username=session['username'])
        else:
            msg = 'Неверный логин или пароль!'
    return render_template('login.html', msg = msg, value = value)
 
# выход из системы
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# функция регистрации нового пользователя
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email    = request.form['email']
        cursor   = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Пользователь с таким именем уже существует!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Неверный email!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Имя пользователя должно содержать только буквенные символы!'
        elif not username or not password or not email:
            msg = 'Пожалуйста, заполните форму!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'Вы успешно зарегистрировались!'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Пожалуйста, заполните форму!'
    return render_template('register.html', msg = msg)

# функция показа домашней страницы авторизованного пользователя
@app.route('/home_page')
def home_page():
    if 'loggedin' in session:
        # показ пользователю домашней страницы в случае успешной авторизации
        return render_template('home_page.html', username=session['username'])
    # Отправка пользователя на страницу ввода логина и пароля в случае неуспешной авторизации 
    return redirect(url_for('login'))

# функция вывода процентной доли содержания каждой из тональностей среди всех комментариев по выбранному месту досуга
def sentiment(reviews):
        [happy, neutral, sad] = [0, 0, 0]
        for review in reviews:
                if (review[3] == 'positive'):
                   happy = happy + 1 
                elif(review[3] == 'negative'):
                   sad = sad + 1
                else:
                    neutral = neutral + 1
        length = len(reviews)
        if length != 0:
            sad     = round(((sad/length)     * 100))
            happy   = round(((happy/length)   * 100))
            neutral = round(((neutral/length) * 100))
        return (sad, happy, neutral)

# функция, анализирующая тональность комментария пользователя, определяет эмоцию (позитивную, нейтральную или негативную) и её числовой показатель
def predict_emotion(reviews):
        tokenizer = RegexTokenizer()
        model     = FastTextSocialNetworkModel(tokenizer=tokenizer)
        text = model.predict([reviews], k = 2)
        for sentiment in text:
            print(list(sentiment.keys())[0])
        emotions = list(sentiment.keys())[0]
        rating   = round(list(sentiment.values())[0], 2)
        return(emotions, rating)

# функция вывода и вставки комментариев пользователей       
@app.route('/comments/<variable>', methods=['GET','POST'])
def comments(variable): 
    acc = []
    place = []
    sentiments = [0, 0, 0]
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT places.id_places, name, link, image, description FROM places WHERE places.id_places = %s', (variable))
    place = cursor.fetchone()

    cursor.execute('SELECT id_places, review, username, emotion FROM reviews, accounts WHERE (reviews.id_places = %s and accounts.id = reviews.id_user)', (variable))
    
    user_emotion = cursor.fetchall()

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'])
    sentiments = sentiment(user_emotion)

    if 'loggedin' in session:
        user_review_query = 'SELECT * FROM reviews WHERE reviews.id_places = % s and reviews.id_user = % s'
        cursor.execute(user_review_query, (variable, session['id']))
        add_comment_user = cursor.fetchall()
        if not add_comment_user:
            if request.method == 'POST':
                comment = request.form['comment']
                if (comment):
                    emotion, rating = predict_emotion(comment)
                    user_id = session['id']
                    insert_query = 'INSERT INTO reviews (id_review, id_user, review, id_places, publication_date, emotion, rating) VALUES (NULL, %s, %s, %s, CURRENT_TIMESTAMP(), %s, %s)'
                    cursor.execute(insert_query, (user_id, comment, variable, emotion, rating))
                    mysql.connection.commit()
                    cursor.close()
                    return redirect(url_for('comments', variable=place[0]))
        else:
            return render_template('user_comments.html', user_emotion=user_emotion, full_filename=full_filename, username=session['username'], place=place, sentiments=sentiments, already_left_review=True)
    cursor.close()
    return render_template('user_comments.html', user_emotion=user_emotion, full_filename=full_filename, place=place, sentiments=sentiments)


if __name__ == '__main__':
    app.run()