import os
from datetime import timedelta
from flask import Flask

from flask import  flash, make_response, request, send_from_directory, redirect, session, url_for, render_template
from flask_login import LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from model.userLogin import UserLogin
from model.services import insertNewClient, insertNewPost
from model.db import get_connection, getUser
from common.config import SECRET_TOKEN, SESSION_LIFETIME_DAYS


__all__ = [
    "app",
]

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'Flask_web-site')
template_dir = os.path.join(template_dir, 'view')
template_dir = os.path.join(template_dir, 'templates')
static_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
static_dir = os.path.join(static_dir, 'Flask_web-site')
static_dir = os.path.join(static_dir, 'view')
static_dir = os.path.join(static_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] =  SECRET_TOKEN # нужен для алгоритма шифрования
app.permanent_session_lifetime = timedelta(days=SESSION_LIFETIME_DAYS)

login_manager = LoginManager(app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('../view/static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
@app.route('/index')
def index():
    # поставить вручную время сессии
    session.permanent = True
    # по умолчанию времяжизни сессии - до закрытия браузера
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return render_template('index.html', session=session)

@app.route('/post_create', methods=["POST",'GET'])
def post_create():
    connection = get_connection()
    if request.method == 'POST':
        name = request.form['name']
        preview = request.form['preview']
        text_message = request.form['text_message']
        if len(preview) == 0:
            preview = text_message[:20]+'...'

        post = {'name':name,'preview':preview,'text_message':text_message}
        insertNewPost(connection, post)

        return redirect('/posts')
    else:
        return render_template('post_create.html')

@app.route('/about')
def about():
    return render_template('about.html')

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return getUser(user_id)

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM `clients` WHERE email = '{request.form['email']}';")
                user = cursor.fetchall()[0]
                cursor.close()
                if user and check_password_hash(user['password'], request.form['password']):
                    userlogin = UserLogin().create(user)
                    login_user(userlogin)
                    return redirect(url_for('index'))
        except Exception as e:
            print(e)
            flash("НЕВЕРНАЯ ПАРА ЛОГИН.ПАРОЛЬ","error")

    return render_template("login.html")

@app.route('/register', methods=["POST","GET"])
def register():
    connection = get_connection()
    if request.method == "POST":
        if len(request.form['name']) > 4 and  len(request.form['email']) > 4 \
            and len(request.form['password']) > 4 \
            and (request.form['password'] == request.form['password2']):
            hash = generate_password_hash(request.form['password'])
            res = insertNewClient(connection, request.form['name'], request.form['email'], hash)
            if res:
                flash('Вы успешно зарегестрированы', 'success')
                return redirect(url_for('login'))
            else:
                flash('Ошибка при добавление в бд', 'error')
        else:
            flash('Неверно заполнены поля','error')
    return render_template("register.html")

@app.route('/logout')
def logout():
    res = make_response("<h1>вы больше не авторизованы</h1>")
    res.set_cookie("logged", "", 0)
    return res

@app.route('/posts')
def posts():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT *\
                FROM posts\
                ORDER BY created_at;")
            result = cursor.fetchall()
            cursor.close()
    except Exception as ex:
        result = None
        print(ex)
    return render_template('posts.html', result=result)

@app.route('/posts/<int:id>')
def post(id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * \
                FROM `web-site`.`posts` \
                WHERE id = {id};")
            result = cursor.fetchall()[0]
            cursor.close()
    except Exception as ex:
        result = None
        print(ex)
    return render_template('post.html',result=result)

@app.route('/posts/<int:id>/delete')
def post_delete(id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM `web-site`.`posts`\
                WHERE (`id` = '{id}');")
            connection.commit()
            cursor.close()
    except Exception as ex:
        print(ex)
    return redirect('/posts')

@app.route('/posts/<int:id>/update', methods=["POST",'GET'])
def post_update(id):
    connection = get_connection()

    if request.method == 'POST':
        if request.form['name'] != '':
            name = request.form['name']
        if request.form['preview'] != '':
            preview = request.form['preview']
        if request.form['text_message'] != '':
            text_message = request.form['text_message']
        try:
            with connection.cursor() as cursor:
                if request.form['name'] != '':
                    cursor.execute("UPDATE posts\
                        SET name=%s WHERE id = %s;",
                        (name,id))
                if request.form['preview'] != '':
                    cursor.execute("UPDATE posts\
                        SET preview=%s WHERE id = %s;",
                        (preview,id))
                if request.form['text_message'] != '':
                    cursor.execute("UPDATE posts\
                        SET text_message=%s WHERE id = %s;",
                        (text_message,id))
                connection.commit()
                cursor.close()
        except Exception as e:
            print(e)
        return redirect('/posts')
    else:
        return render_template('post_update.html',id=id)

@app.errorhandler(404)
def pageNot(error):
    return ("Страница не найдена", 404)
