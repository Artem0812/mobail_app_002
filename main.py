import psycopg2
import re

import self as self
from psycopg2 import Error
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

from kivy.config import Config
Window.size = (480, 790)
Config.set('graphics', 'resizable', True)


class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                user="postgres",
                password="1",
                host="127.0.0.1",
                port="5432",
                database="BD_Test"
            )
            self.cur = self.conn.cursor()


            self.cur = self.conn.cursor()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def query_password(self, index):
        try:
            self.cur.execute(f'''SELECT u_passw, u_name FROM users
                                WHERE u_id = '{index}' 
                                        ''')

            self.rows = self.rowUnpacker(self.cur.fetchall())
            return self.rows

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def create_users(self, passwdText, nameText):
        try:
            self.cur.execute(f'''INSERT INTO users ( u_name, u_passw) 
                                    VALUES ('{nameText}', '{passwdText}') ''')
            self.conn.commit()


        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()
    def check(self):
        try:
            self.cur.execute(f'''SELECT u_id FROM users ORDER BY u_id DESC LIMIT 1 ''')
            self.rows = self.rowUnpacker(self.cur.fetchall())
            return self.rows
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def questions(self, index):
        try:
            self.cur.execute(f'''SELECT q_ques, answers.a_answer FROM questions
                                JOIN answers ON questions.q_id = answers.a_id
                                WHERE q_id = '{index}' 
                                        ''')
            self.rows = self.rowUnpacker(self.cur.fetchall())
            print(self.rows)
            return self.rows

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def creat_column(self, new_column_name):
        try:
            self.cur.execute(f'''ALTER TABLE results ADD COLUMN {new_column_name} integer''')
            self.conn.commit()

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()
    def check_column(self):
        try:
            self.cur.execute(f'''SELECT column_name
                                 FROM information_schema.columns
                                 WHERE table_name = 'results' ''')
            self.rows = self.rowUnpacker(self.cur.fetchall())
            print(self.rows)
            return self.rows
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def result(self, user, index):
        try:
            self.cur.execute(f'''SELECT {user} FROM users
                                WHERE '{index}' 
                                        ''')

            self.rows = self.rowUnpacker(self.cur.fetchall())
            return self.rows

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def last_column(self):
        try:
            self.cur.execute(f'''SELECT column_name
                                FROM information_schema.columns
                                WHERE table_name = 'results'
                                ORDER BY ordinal_position DESC LIMIT 1''')
            self.rows = self.rowUnpacker(self.cur.fetchall())
            print("последний столбец",self.rows)
            self.conn.commit()
            return self.rows


        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()
    def i_o_row(self, user, num):
        try:
            self.cur.execute(f'''INSERT INTO results  ({user}) 
                                    VALUES ({num}) ''')
            self.conn.commit()


        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def check_answers(self, user):
        try:
            self.cur.execute(f'''SELECT COALESCE({user}, 0) FROM results''')
            self.rows = self.rowUnpacker(self.cur.fetchall())
            print("ответы",self.rows)
            return self.rows
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def check_res(self, user):
        try:
            self.cur.execute(f'''SELECT {user} FROM results''')

            self.rows = self.rowUnpacker(self.cur.fetchall())
            print(self.rows)
            return self.rows

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def query_res(self, index):
        try:
            self.cur.execute(f'''SELECT u_res FROM users
                                 
                                        ''')

            self.rows = self.rowUnpacker(self.cur.fetchall())
            return self.rows
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def create_users_ras(self, nameText):
        try:
            self.cur.execute(f'''UPDATE users SET u_res = '{nameText}'
                                     ''')
            self.conn.commit()


        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            self.connection_close()

    def connection_close(self):
        if self.conn:
            self.cur.close()
            self.conn.close()

    def rowUnpacker(self, rows):
        unpackRow = []
        for row in rows:
            for name in row:
                unpackRow.append(name)
        return unpackRow

class MainApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(Entrance(name="first"))
        sm.add_widget(Registration(name="Registr"))
        sm.add_widget(Authorization(name="Auth"))
        sm.add_widget(Test(name="Test"))
        sm.add_widget(Testwo(name="Testwo"))
        sm.add_widget(Testhree(name="Testhree"))
        sm.add_widget(Testfour(name="Testfour"))
        sm.add_widget(Testfive(name="Testfive"))
        sm.add_widget(result(name="result"))
        sm.add_widget(resultwo(name="resultwo"))

        return sm


class Entrance(Screen):
    def first_main(self):
        sm = self.manager
        sm.transition.direction = 'left'
        sm.current = 'Registr'
    def Auth(self):
        sm = self.manager
        sm.transition.direction = 'left'
        sm.current = 'Auth'

class Registration(Screen):
    def entr (self):
        if self.passwd.text == "" or self.nam.text == "":
            self.label.text = "Заполните все поля"
        else:
            Database().create_users(self.passwd.text, self.nam.text)
            self.column = Database().check_column()
            for clmn in self.column:
                if self.nam.text == clmn:
                    self.label.text = "Имя уже существует"
                    print("регистрация",clmn)
                    break
            else:
                print("Новое слово:")
                Database().creat_column(self.nam.text)
                print("регистрация",self.nam.text)
                colum = self.nam.text
                sm = self.manager
                sm.transition.direction = 'left'
                sm.current = 'Test'




class Authorization(Screen):


    def ladel_function_text(self):
        self.lastindex = Database().check()
        self.firstindex = 1
        print("это",self.lastindex)
        self.column = Database().check_column()
        for clmn in self.column:
            if self.nam.text == clmn:
                print("колонка", clmn)
                self.label.text = "Имя уже существует"
                self.manager.transition.direction = 'left'
                self.manager.current = 'resultwo'
                break


            for _ in range(self.lastindex[0]):
                    self.textNP = Database().query_password(self.firstindex)
                    print(self.textNP)
                    if self.passwd.text == self.textNP[0] and self.nam.text == self.textNP[1]:
                        self.manager.transition.direction = 'left'
                        self.manager.current = 'Test'
                        break

                    else:
                        self.firstindex +=1

                        self.label.text = "Не верно"

class Test(Screen):
    def But1(self):
        self.rows = Database().last_column()
        i = 0
        Database().i_o_row(self.rows[0], i)
        self.manager.transition.direction = 'left'
        self.manager.current = 'Testwo'


    def But2(self):
        self.rows = Database().last_column()
        i = 1
        Database().i_o_row(self.rows[0], i)
        self.manager.transition.direction = 'left'
        self.manager.current = 'Testwo'


class Testwo(Screen):
    def But1(self):
        self.rows = Database().last_column()
        i = 0
        Database().i_o_row(self.rows[0], i)
        self.manager.transition.direction = 'left'
        self.manager.current = 'Testhree'

    def But2(self):
        self.rows = Database().last_column()
        i = 1
        Database().i_o_row(self.rows[0], i)
        self.manager.transition.direction = 'left'
        self.manager.current = 'Testhree'

class Testhree(Screen):
    def But1(self):
        self.rows = Database().last_column()
        i = 1
        Database().i_o_row(self.rows[0], i)
        self.manager.transition.direction = 'left'
        self.manager.current = 'Testfour'

    def But2(self):
        self.rows = Database().last_column()
        i = 0
        Database().i_o_row(self.rows[0], i)
        self.manager.transition.direction = 'left'
        self.manager.current = 'Testfour'

class Testfour(Screen):
    def But1(self):
        self.rows = Database().last_column()
        i = 1
        Database().i_o_row(self.rows[0], i)
        self.manager.transition.direction = 'left'
        self.manager.current = 'Testfive'

    def But2(self):
        self.rows = Database().last_column()
        i = 0
        Database().i_o_row(self.rows[0], i)
        self.manager.transition.direction = 'left'
        self.manager.current = 'Testfive'

class Testfive(Screen):
    def But1(self):
        self.rows = Database().last_column()
        i = 1
        Database().i_o_row(self.rows[0], i)
        self.manager.transition.direction = 'left'
        self.manager.current = 'result'

    def But2(self):
        self.rows = Database().last_column()
        i = 0
        Database().i_o_row(self.rows[0], i)
        self.manager.transition.direction = 'left'
        self.manager.current = 'result'


class result(Screen):
    def res(self):
        self.rows = Database().last_column()
        self.res_rows = Database().check_res(self.rows[0])
        self.R = Database().check_answers(self.rows[0])
        sum_digits = 0
        for num in self.R:
            print(num)
            # добавляем значение текущей цифры к сумме
            sum_digits += int(num)
        # выводим итоговую сумму
        print(f"Сумма ",sum_digits)
        if sum_digits == 5:

            self.label.text = "Вы Космонавт"
        else:
            self.label.text = "Ты... не готов"
            Database().create_users_ras(self.label.text)

class resultwo(Screen):
    def res(self):
        self.lastindex = Database().check()
        self.firstindex = 1
        print("это последний", self.lastindex)
        for _ in range(self.lastindex[0]):
            self.textNP = Database().query_res(self.firstindex)
            print(self.textNP)



            self.firstindex += 1
        self.label.text = str(self.textNP[0])


if __name__ == '__main__':
    MainApp().run()



