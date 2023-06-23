from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///shop_data.db'
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_RECORD_QUERIES"] = True

db = SQLAlchemy(app)

class Mainmenu(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(50),nullable = True)
    url = db.Column(db.String(50),nullable = True)

    def __repr__(self):
        return f"<mainmenu {self.id}>"

class Products(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(150),nullable = True)
    price = db.Column(db.Integer,nullable = True)
    descript = db.Column(db.Text(500),nullable = True)
    table_n = db.Column(db.String(150),nullable = True)
    product_photo = db.Column(db.String ,nullable = True)
    post_date = db.Column(db.DateTime,default = datetime.utcnow())

    def __repr__(self):
        return f"<products {self.id}>"

class Shop_menu(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(50),nullable = True)
    url = db.Column(db.String(50),nullable = True)
    table_n = db.Column(db.String,nullable = True)

    def __repr__(self):
        return f"<shopmenu {self.id}>"

class Users(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    login = db.Column(db.String(50) , unique = True)
    password = db.Column(db.String(500),nullable = True)
    phone = db.Column(db.String(12))
    avatar = db.Column(db.LargeBinary , nullable = True)

    def __repr__(self):
        return f"<users {self.id}>"

# Создать БД
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
