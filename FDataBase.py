import math , time , sqlite3

class FDataBase:
    def __init__(self,db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = ''' SELECT * FROM mainmenu '''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                print(res)
                return res
        except:
            print("Ошибка чтения БД")
        return ['no']

    def get_shop_menu(self):
        sql = ''' SELECT * FROM shop_menu '''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения БД")
        return ['no']

    # Товары в магазин ( доделать )
    def get_all_products(self):
        sql = '''SELECT * FROM products'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения товаров из БД")
        return ['no']

    # Товары под категориями
    def get_categ_products(self,table):
        try:
            self.__cur.execute(f"SELECT * FROM products WHERE table_n = '{table}'")
            res = self.__cur.fetchall()
            if res:
                # print(res)
                return res
        except sqlite3.Error as e:
            print("Error " + str(e))
        return (False,False)

    # Добавить запись
    def add_post(self,name,price,descr,table,photo):
        try:
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO products VALUES(NULL,?,?,?,?,?,?)',(name,price,descr,table,photo,tm))
            self.__db.commit()
            print("Успешно !")
        except sqlite3.Error as e:
            print('ошбка добавления статьи'+str(e))
            return False
        return True

    # Удаление статьи через админ панель
    def delete_post(self,post_id):
        sql = f""" DELETE FROM products WHERE id = {post_id} """
        try:
            self.__cur.execute(sql)
            self.__db.commit()
        except sqlite3.Error as e:
            print('ошибка удаления статьи '+str(e))
            return False
        return True

    def delete_user(self,id):
        sql = f"DELETE FROM users WHERE id = {id}"
        try:
            self.__cur.execute(sql)
            self.__db.commit()
        except sqlite3.Error as e:
            print('ошибка удаления пользоваетля '+str(e))
            return False
        return True

    # Открыть пост
    def get_post(self,post_id):
        try:
            self.__cur.execute(f"SELECT * FROM products WHERE id = {post_id} LIMIT 1")
            res = self.__cur.fetchone()
            if res: return res
        except sqlite3.Error as e:
            print("Error" +str(e))
        return False

    # Доавбление пользователя в БД
    def add_user(self,login,phone,psw):
        try:
            self.__cur.execute(" INSERT INTO users VALUES (NULL,?,?,?)",(login,phone,psw))
            self.__db.commit()
        except sqlite3.Error as e:
            print('ошбка добавления статьи '+str(e))
            return False
        return True

    # Получение пользователей из БД
    def get_users(self):
        sql = """ SELECT login FROM users """
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                # print("Users", res[0]['login'])
                return res
        except sqlite3.Error as e:
            print("Error " +str(e))
        return (False,False)

    def get_user(self,login):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден" , res)
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получени данных из БД " +str(e))
        return False

#10- 13:40 - фото
