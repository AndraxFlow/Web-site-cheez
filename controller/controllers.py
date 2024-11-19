import os
from datetime import timedelta
from flask import Flask, Response

from flask import  flash, make_response, request, send_from_directory, redirect, session, url_for, render_template
from flask_login import LoginManager, current_user, login_required, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from model.userLogin import UserLogin
from model.db import get_connection
from model.FDatabase import FDatabase
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
app.config['TESTING'] = False
app.config['LOGIN_DISABLED'] = False
app.permanent_session_lifetime = timedelta(days=SESSION_LIFETIME_DAYS)

login_manager = LoginManager()
login_manager.init_app(app=app)
login_manager.login_view = 'login'

@app.route('/favicon.ico')
def favicon() -> Response:
    return send_from_directory('../view/static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.before_request
def before_request():
    global db, connection
    connection = get_connection()
    db = FDatabase(db=connection)
    
@app.teardown_appcontext
def close_db(error):
    '''Закрытие соединения с бд'''
    if connection:
        db.closeConnect()
    

@app.route('/')
@app.route('/index')
def index() :
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
    if not current_user.is_authenticated:
        flash('Пожалуйста, войдите в систему, чтобы получить доступ к этой странице.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        preview = request.form['preview']
        text_message = request.form['text_message']
        # owner_id = db.getUser()
        if len(preview) == 0:
            preview = text_message[:20]+'...'
        post = {'name':name,'preview':preview,'text_message':text_message}
        
        res = db.insertNewPost(post=post)
        if res:
            flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка в добавлении статьм', category='error')

        return redirect('/posts')
    else:
        return render_template('post_create.html')

@app.route('/about')
def about():
    return render_template('about.html')

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id=user_id, db=db)



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        user = db.getUserByEmail(request.form['email'])
        
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('index'))

    return render_template("login.html")

@app.route('/register', methods=["POST","GET"])
def register():
    if request.method == "POST":
        if len(request.form['name']) > 4 and  len(request.form['email']) > 4 \
            and len(request.form['password']) > 4 \
            and (request.form['password'] == request.form['password2']):
            hash = generate_password_hash(request.form['password'])
            
            res = db.insertNewClient( request.form['name'], request.form['email'], hash)
            
            if res:
                flash('Вы успешно зарегестрированы', 'success')
                return redirect(url_for('login'))
            else:
                flash('Ошибка при добавление в бд', 'error')
        else:
            flash('Неверно заполнены поля','error')
    return render_template("register.html")

@app.route('/logout')
@login_required
def logout():
    res = make_response("<h1>вы больше не авторизованы</h1>")
    res.set_cookie("logged", "", 0)
    return res

@app.route('/posts')
def posts():
    result = db.getPosts()
    return render_template('posts.html', result=result)

@app.route('/posts/<int:id>')
@login_required
def post(id):
    result = db.getPost(id_post=id)
    return render_template('post.html',result=result)

@app.route('/posts/<int:id>/delete')
@login_required
def post_delete(id):
    db.deletePost(id_post=id)
    return redirect('/posts')

@app.route('/posts/<int:id>/update', methods=["POST",'GET'])
@login_required
def post_update(id):
    if request.method == 'POST':
        name = ''
        preview = ''
        text_message = ''
        if request.form['name'] != '':
            name = request.form['name']
        if request.form['preview'] != '':
            preview = request.form['preview']
        if request.form['text_message'] != '':
            text_message = request.form['text_message']
        
        db.updatePost(id_post=id,name=name,preview=preview, text_message=text_message)
        
        return redirect('/posts')
    else:
        return render_template('post_update.html',id=id)

@app.errorhandler(404)
def pageNot(error):
    return ("Страница не найдена", 404)
