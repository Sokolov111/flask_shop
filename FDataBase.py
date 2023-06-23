import math , time , sqlite3
import app_file

class FDataBase:
    def __init__(self,db):
        self.__db = db
        # self.__cur = db.cursor()

    def get_menu(self):
        try:
            with app_file.app.app_context():
                res = app_file.Mainmenu.query.all()
                if res:
                    return res
        except:
            app_file.db.session.rollback()
            print("Error 18str")

    def get_shop_menu(self):
        try:
            with app_file.app.app_context():
                res = app_file.Shop_menu.query.all()
                if res:
                    return res
        except:
            app_file.db.session.rollback()
            print("Error 27str")

    def get_all_products(self):
         try:
            with app_file.app.app_context():
                res = app_file.Products.query.all()
                if res:
                    return res
         except:
             print("Error 36str")
         return ['no']
        # sql = '''SELECT * FROM products'''
        # try:
        #     self.__cur.execute(sql)
        #     res = self.__cur.fetchall()
        #     if res: return res
        # except:
        #     print("Ошибка чтения товаров из БД")
        # return ['no']

    # Товары под категориями
    def get_categ_products(self,table):
        try:
            with app_file.app.app_context():
                res = app_file.Products.query.filter_by(table_n = table).all()
                if res:
                    return res
        except:
            print("Error 55str")

        # self.__cur.execute(f"SELECT * FROM products WHERE table_n = '{table}'")
        #     res = self.__cur.fetchall()
        #     if res:
        #         # print(res)
        #         return res
        # except sqlite3.Error as e:
        #     print("Error " + str(e))
        # return (False,False)

    # Добавить запись
    def add_post(self,name,price,descr,table,photo):
        with app_file.app.app_context():
            try:
                # tm = math.floor(time.time())
                p = app_file.Products(name= name, price= price, descript=descr,table_n=table,product_photo=photo)
                app_file.db.session.add(p)
                app_file.db.session.flush()
                app_file.db.session.commit()
            except sqlite3.Error as e:
                app_file.db.session.rollback()
                print("Ошибка добавления поста" , e)
                return False
            return True
        # try:
        #     tm = math.floor(time.time())
        #     self.__cur.execute('INSERT INTO products VALUES(NULL,?,?,?,?,?,?)',(name,price,descr,table,photo,tm))
        #     self.__db.commit()
        #     print("Успешно !")
        # except sqlite3.Error as e:
        #     print('ошбка добавления статьи'+str(e))
        #     return False
        # return True

    def add_user(self,flogin,fpsw,fphone):
        try:
            with app_file.app.app_context():
                u = app_file.Users(login = flogin  , password = fpsw, phone = fphone)
                app_file.db.session.add(u)
                app_file.db.session.flush()
                app_file.db.session.commit()
        except sqlite3.Error as e:
            app_file.db.session.rollback()
            print("Ошибка регистрации" , e)
            return False
        return True
        # try:
        #     self.__cur.execute(" INSERT INTO users VALUES (NULL,?,?,?,NULL)",(login,phone,psw))
        #     self.__db.commit()
        # except sqlite3.Error as e:
        #     print('ошбка добавления статьи '+str(e))
        #     return False
        # return True

    # Удаление статьи через админ панель
    def delete_post(self,post_id):
        try:
            with app_file.app.app_context():
                from sqlalchemy import delete
                delete_stmt = (
                    delete(app_file.Users)
                    .where(app_file.Users.id == post_id)
                )
                # if delete_stmt:
                #     print("Успешно")
                # else:
                #     print("Неуспешно")
                # delete(app_file.Users).where(app_file.Users == post_id)

                # app_file.Users.query(app_file.Users).filter_by(id = post_id).delete(synchronize_session = 'fetch')

                app_file.db.session.commit()

        except sqlite3.Error as e:
            print("Ошибка удаления поста " ,e)
            app_file.db.session.rollback()
            return False
        return True

        # sql = f""" DELETE FROM products WHERE id = {post_id} """
        # try:
        #     self.__cur.execute(sql)
        #     self.__db.commit()
        # except sqlite3.Error as e:
        #     print('ошибка удаления статьи '+str(e))
        #     return False
        # return True

    def delete_user(self , user_id):
        try:
            with app_file.app.app_context():
                from sqlalchemy import delete
                delete(app_file.Users).where(app_file.Users == user_id)
                # user = app_file.Users.query.get(user_id)
                # app_file.db.session.delete(user)
                app_file.db.session.commit()
        except sqlite3.Error as e:
            print("Ошибка удаления пользователя ",e)
            app_file.db.session.rollback()
            return False
        return True

        # sql = f"DELETE FROM users WHERE id = {user_id}"
        # try:
        #     self.__cur.execute(sql)
        #     self.__db.commit()
        # except sqlite3.Error as e:
        #     print('ошибка удаления пользоваетля '+ str(e))
        #     return False
        # return True

    # Открыть пост
    def get_post(self,post_id):
        try:
            with app_file.app.app_context():
                res = app_file.Products.query.filter_by(id = post_id).all()
                if res:
                    return res
        except:
            print("Error 107")

        # try:
        #     self.__cur.execute(f"SELECT * FROM products WHERE id = {post_id} LIMIT 1")
        #     res = self.__cur.fetchone()
        #     if res: return res
        # except sqlite3.Error as e:
        #     print("Error" +str(e))
        # return False

    # Доавбление пользователя в БД


    # Получение пользователей из БД
    def get_users(self,login):
        try:
            with app_file.app.app_context():
                res = app_file.Users.query.filter_by(login=login).all()
                if res:
                    return True
        except:
            app_file.db.session.rollback()
            print("Error 113str")
        return False

        # sql = """ SELECT login FROM users """
        # try:
        #     self.__cur.execute(sql)
        #     res = self.__cur.fetchall()
        #     if res:
        #         # print("Users", res[0]['login'])
        #         return res
        # except sqlite3.Error as e:
        #     print("Error " + str(e))
        # return (False,False)

    def get_users_by_login(self,login):
        try:
            with app_file.app.app_context():
                res = app_file.Users.query.filter_by(login = login).limit(1).all()
                if res:
                    print(res[0].password)
                    return res
        except:
            app_file.db.session.rollback()
            print("Error 134str")

        # try:
        #     self.__cur.execute(f"SELECT * FROM users WHERE login = '{login}'")
        #     res = self.__cur.fetchone()
        #     if not res:
        #         print("Ошибка получения пользователей")
        #         return False
        #     return res
        # except sqlite3.Error as e:
        #     print("Ошибка получени данных по пользователям из БД " +str(e))
        # return False

    def get_user(self,user_id):
        try:
            with app_file.app.app_context():
                res = app_file.Users.query.filter_by(id = user_id).limit(1).all()
                if res:
                    # print("165 res:  ", res)
                    return res
        except:
            app_file.db.session.rollback()
            print("Error 155str")

        # try:
        #     self.__cur.execute(f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
        #     res = self.__cur.fetchone()
        #     if not res:
        #         print("Пользователь не найден" , res)
        #         return False
        #     return res
        # except sqlite3.Error as e:
        #     print("Ошибка получения данных из БД " + str(e))
        # return False

    # Обновление фото пользователя в БД

    def updateUserAvatar(self,avatar,user_id):
        if not avatar:
            return False

        binary = sqlite3.Binary(avatar)
        try:
            with app_file.app.app_context():
                res = app_file.Users.query.filter_by(id = user_id).update({"avatar":avatar}, synchronize_session='fetch')
                app_file.db.session.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления фото " , e)
            return False

        return True

        # try:
        #     binary = sqlite3.Binary(avatar)
        #     self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?",(binary,user_id))
        #     self.__db.commit()
        # except sqlite3.Error as e:
        #     print("Ошибка обновления данных в БД " + str(e))
        #     return False

        # return True
