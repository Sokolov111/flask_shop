import flask as fl
from DBFile import get_db
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import LoginManager , login_user , login_required ,logout_user , current_user
from UserLogin import UserLogin


app = fl.Flask(__name__)
app.config["SECRET_KEY"] = "ASGKASJFQ3323AKFSFK32FKAF"

login_manager = LoginManager(app)
login_manager.login_message = "Авторизуйтесь для доступа к странице"
login_manager.login_message_category = "success"
login_manager.login_view = 'login'

menu = [{"url":"/",'name':'Главная'},
        {"url":"/posts",'name':'Посты'},
        {"url":"/about",'name':'О нас'},
        {"url":"/login",'name':'Кабинет'}]


# Функция для получения данных из БД
dbase = None
@app.before_request
def DBase_connect():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

# Главная страница
@app.route('/')
@app.route("/index")
def index():
    # if 'userLogged' in fl.session:
    #     user_name = fl.session['userLogged']
    # else:
    #     user_name = "None"

    return fl.render_template("index.html",menu = dbase.get_menu(), title= "Главная")

# Регистрация
@app.route('/registration', methods=["GET","POST"])
def registration():
    user_in_base = True
    if fl.request.method == "POST":
        for i in range(len(dbase.get_users())):
            if fl.request.form['login'] == dbase.get_users()[i][0]:
                print("Пользователь с таким логином уже есть !" , dbase.get_users()[i][0])
                fl.flash("Пользователь с таким логином уже есть !",category='error')
                user_in_base = False
                break
            else:
                print("else")

        if user_in_base:
            if len(fl.request.form['psw']) < 9 or fl.request.form['psw'] != fl.request.form['rep_psw']:
                fl.flash("Пароль неверный",category='error')
            else:
                # Шифрование пароля
                hpsw = generate_password_hash(fl.request.form['psw'])
                res = dbase.add_user(fl.request.form['login'],hpsw,fl.request.form['telephone'])
                if not res:
                    fl.flash("Ошибка добавления статьи",category = "error")
                else:
                    fl.flash("Успешно! ",category = 'success')
                    return fl.redirect(fl.url_for('login'))

    # return fl.render_template('add_post.html',menu = dbase.get_menu())

    return fl.render_template('/registration.html' , menu=dbase.get_menu())

@login_manager.user_loader
def load_user(user_id):
    print("Load user")
    return UserLogin().fromDB(user_id,dbase)


# Логинизация ( доделать )
@app.route('/login',methods = ["POST","GET"])
def login():
    if current_user.is_authenticated:
        return fl.redirect(fl.url_for('kabinet'))

    if fl.request.method == "POST":
        user = dbase.get_user(fl.request.form['login'])
        if user:
            userLogin = UserLogin().create(user)
            rm = True if fl.request.form.get('remainme') else False
            login_user(userLogin,remember=rm)
            return fl.redirect(fl.url_for('kabinet'))
        elif fl.request.form['login'] == "admin" and fl.request.form['pwd'] == '123':
            userLogin = UserLogin().create(user)
            fl.flash("Данные верны !",category="success")
            rm = True if fl.request.form.get('remainme') else False
            login_user(userLogin,remember=rm)
            return fl.redirect(fl.url_for('admin'))
        fl.flash("Неверно введены логин/пароль",category='error')
    return fl.render_template('login.html',menu=dbase.get_menu())


    # ----------------------------------------------->
    # Ошибка - найти обход fl.request.form['login']
    # user_map = fl.request.form['login'] if fl.request.form['login'] in map(str,dbase.get_users()) else 'False'

    # Проверка - правильно ли отправлены данные
    # if "userLogged" in fl.session:
    #     # fl.session['userLogged'] = fl.request.form['login']
    #     fl.flash("Данные верны !",category="success")
    #     return fl.redirect(fl.url_for('kabinet',username = fl.session['userLogged']))
    #
    # # Ошибка - найти обход fl.request.form['login']
    # # elif user_map:
    # #     fl.session['userLogged'] = fl.request.form['login']
    # #     return fl.redirect(fl.url_for('kabinet',username = fl.session['userLogged']))
    #
    # # если такой юзер в БД есть -
    # elif fl.request.method == "POST" and fl.request.form['login'] == "admin" and fl.request.form['pwd'] == '123':
    #     # Создать сессию
    #     fl.session['userLogged'] = fl.request.form['login']
    #     fl.flash("Данные верны !",category="success")
    #     return fl.redirect(fl.url_for('admin',username = fl.session['userLogged']))
    # # elif user_in_base:
    # #     fl.session['userLogged'] = fl.request.form['login']
    # #     return fl.redirect(fl.url_for('kabinet',username = fl.session['userLogged']))
    # else:
    #     fl.flash("Повторите поптытку",category="error")
    #
    # return fl.render_template('login.html',menu = menu)

# Админ панель
@app.route('/admin')
def admin():
    # Проверка на неправильный путь до пользователя
    # if "userLogged" not in fl.session or fl.session["userLogged"] != username:
    #     fl.abort(401)

    admin_menu =  dbase.get_menu()
    return fl.render_template('admin_panel.html',menu =admin_menu,title='Личный кабинет')


# ЛК ( доделать )
@app.route('/kabinet')
@login_required
def kabinet():
    # Проверка на неправильный путь до пользователя
    # if "userLogged" not in fl.session or fl.session["userLogged"] != username:
    #     fl.abort(401)

    return fl.render_template('kabinet.html',menu = dbase.get_menu(),title='Личный кабинет' )

# Выход из ЛК
@app.route('/logout')
def logout():
    logout_user()
    fl.flash('Вы вышли из аккаунта','success')

    return fl.redirect(fl.url_for('login'))

# Для примера - вывод постов
@app.route('/post/<int:id_post>')
def show_post(id_post):
    if 'userLogged' in fl.session:
        user_name = fl.session['userLogged']
    else:
        user_name = "None"

    obj = dbase.get_post(id_post)

    if not obj:
        fl.abort(404)

    return fl.render_template('post.html',menu=dbase.get_menu() , name = obj , user = user_name )

# Вкладка магазин

@app.route("/shop")
@login_required
def shop_page():

    return fl.render_template('shop.html',menu = dbase.get_menu(), shop_menu = dbase.get_shop_menu(),products = dbase.get_all_products(), title= "Магазин")

# Вкладка постов под категориями
@app.route("/shop/<table_n>")
def category_post(table_n):
    name = dbase.get_categ_products(table_n)
    return fl.render_template('phones.html',menu=dbase.get_menu(), shop_menu = dbase.get_shop_menu(),title='Телефоны',name = name )

# Удаление поста через админ панель
@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    Dbase = dbase.delete_post(post_id)
    return fl.render_template('index.html',menu=dbase.get_menu(),title = "Главная")

# Удалить пользоваетя
@app.route('/delete_user', methods = ["GET","POST"])
def delete_user():

    id_ = fl.request.form.get('user_id')
    print(id)
    del_user = FDataBase.delete_user(id_)
    if not del_user:
        fl.flash("Ошибка добавления статьи",category = "error")
    else:
        fl.flash("Успешно! ",category = 'success')
        return fl.redirect(fl.url_for('admin_panel'))
    return fl.render_template('admin_panel.html',menu=dbase.get_menu(),title = "Админ панель")



@app.route('/create_post',methods = ["POST","GET"])
def create_post():
    if fl.request.method == "POST":
        print("POST")
        res = dbase.add_post(fl.request.form['name'],fl.request.form['price'],fl.request.form['descript'],fl.request.form['table_n'],fl.request.form['pord_photo'])
        if not res:
            fl.flash("Ошибка добавления статьи",category = "error")
        else:
            fl.flash("Успешно! ",category = 'success')

    return fl.render_template('create_post.html')

# ошибка при неправильном переходе
@app.errorhandler(404)
def not_found(error):
    return fl.render_template("not_found.html",menu=menu,title="Страница не найдена!")

# 14 логин - регистрация






#  Разрыв соединения с БД
@app.teardown_appcontext
def close_db(error):
    if hasattr(fl.g,'link_db'):
        fl.g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)

# 15 - нужно сделать , доступ юзеров к постам
