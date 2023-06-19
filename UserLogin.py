from flask_login import UserMixin
import flask as fl

class UserLogin(UserMixin):
    def fromDB(self,user_id , db):
        self.__user = db.get_user(user_id)
        return self

    def create(self,user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def get_name(self):
        return self.__user['login'] if self.__user else "Без Логина"

    def get_phone(self):
        return self.__user['phone'] if self.__user else "Без Номера"

    # получить аватарку в ЛК
    def get_avatar(self,app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + fl.url_for('static',filename = 'images/default.png') , 'rb') as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию" + str(e))
        else:
            img = self.__user['avatar']
        return img

    # Проверить что формат извображения png/PNG
    def verifyExt(self,filename):
        ext = filename.rsplit('.',1)[1]
        if ext == "png" or ext == "PNG":
            return True
        return False
