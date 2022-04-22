import sqlite3
import datetime

#day = '2022-05-04'
#num = 1

class Costs:

    def create_costs(self):
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS prices(
            my_order_cost REAL,
            my_pos_cost REAL);
        ''')
        data = self.cursor.execute('''SELECT * FROM prices''').fetchone()
        if data == None:
            self.cursor.execute(
                '''INSERT INTO prices(my_order_cost, my_pos_cost) VALUES (?, ?);''',
                (30, 7.5))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def update_costs(self, ord_cost):
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            '''INSERT INTO prices(my_order_cost, my_pos_cost) VALUES (?, ?);''',
            ord_cost)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def delete_costs(self):
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''DELETE FROM prices''')
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def select_ord_cost(self):
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()
        today_price = self.cursor.execute('''SELECT * FROM prices''').fetchone()
        ord_c = today_price[0]
        self.cursor.close()
        self.connection.close()
        return str(ord_c)

    def select_pos_cost(self):
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()
        today_price = self.cursor.execute('''SELECT * FROM prices''').fetchone()
        pos_c = today_price[1]
        self.cursor.close()
        self.connection.close()
        return str(pos_c)


class Orders:

    def __init__(self):
        self.orders = 0
        self.positions = 0
        self.date = datetime.date.today()
        self.income = 0
        self.weekday = datetime.datetime.today().isoweekday()
        self.session = (self.orders, self.positions, self.date, self.income,
                    self.weekday)

    def create_orders(self):
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY,
            my_order INT,
            my_positions INT,
            my_date TEXT,
            my_income REAL,
            my_weekday INT);
        ''')
        self.connection.commit()
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''INSERT INTO orders(my_order, my_positions, 
        my_date,
                                    my_income, my_weekday) VALUES (?, ?, ?, 
                                    ?, ?);''',
                            self.session)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def select_orders(self, ord_cost, pos_cost, new_order):
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()
        rows = self.cursor.execute('''SELECT * FROM orders''')
        for row in rows:
            if row[3] == str(self.date):
                self.orders = row[1] + 1
                self.positions = row[2] + new_order
                self.date = datetime.date.today()
                self.income = row[4] + (ord_cost + pos_cost *
                                   new_order)
                self.weekday = datetime.datetime.today().isoweekday()
                self.session = (self.orders, self.positions, self.date, self.income,
                        self.weekday)
                self.cursor.execute('''DELETE FROM orders WHERE my_date = ?;''',
                               (self.date,))
                self.cursor.execute('''INSERT INTO orders(my_order, my_positions, 
                                    my_date, my_income, my_weekday) VALUES 
                                    (?, ?, ?, ?, ?);''',
                               self.session)
                self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def select_orders_today(self):
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()
        today_tpl = self.cursor.execute('''SELECT * FROM orders WHERE my_date = 
                                        ?;''',(self.date,)).fetchone()
        return today_tpl

    def delete_orders_today(self):
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()

        rows = self.cursor.execute('''SELECT * FROM orders''')
        for row in rows:
            if row[3] == str(self.date):
                self.orders = 0
                self.positions = 0.0
                self.date = datetime.date.today()
                self.income = 0.0
                self.weekday = datetime.datetime.today().isoweekday()
                self.session = (
                self.orders, self.positions, self.date, self.income,
                self.weekday)
                self.cursor.execute('''DELETE FROM orders WHERE my_date = ?;''',
                                    (self.date,))
                self.cursor.execute('''INSERT INTO orders(my_order, 
                my_positions, 
                                            my_date, my_income, my_weekday) 
                                            VALUES 
                                            (?, ?, ?, ?, ?);''',
                                    self.session)
                self.connection.commit()
        self.cursor.close()
        self.connection.close()


class WeeklyOrders:

    def __init__(self):
        self.week_orders = 0
        self.week_positions = 0
        self.week_first_day = ''
        self.week_last_day = ''
        self.week_income = 0
        self.date = datetime.date.today()

    def create_weekly_orders(self):
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS weekly_orders(
            id INTEGER PRIMARY KEY,
            my_orders INT,
            my_positions INT,
            first_day TEXT,
            last_day TEXT,
            my_income REAL);
        ''')
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def update_weekly_orders(self):
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()
        rows = self.cursor.execute('''SELECT * FROM orders''').fetchall()
        first_tuple = self.cursor.execute('''SELECT * FROM orders''').fetchone()
        week_list = []
        week_list.append(first_tuple)
        for row in rows:
            last_tuple = week_list[-1]
            if row[5] > last_tuple[5]:
                week_list.append(row)
            elif row[5] < last_tuple[5]:
                for tpl in week_list:
                    self.week_orders += tpl[1]
                    self.week_positions += tpl[2]
                    self.week_first_day = week_list[0][3]
                    self.week_last_day = week_list[-1][3]
                    self.week_income += tpl[4]
                self.week_session = (
                self.week_orders, self.week_positions, self.week_first_day, self.week_last_day,
                self.week_income)

                self.cursor.execute(
                    '''INSERT INTO weekly_orders(my_orders, my_positions, 
                    first_day, last_day, my_income) VALUES (?, ?, ?, ?, ?);''',
                    self.week_session)
                self.connection.commit()

                self.cursor.execute('''DELETE FROM orders WHERE my_date < ?;''',
                               (self.date,))
                self.connection.commit()
                self.cursor.close()
                self.connection.close()

    def select_weekly_orders(self):
        self.connection = sqlite3.connect('income.db')
        self.cursor = self.connection.cursor()
        rows = self.cursor.execute('''SELECT * FROM weekly_orders''').fetchall()
        self.cursor.close()
        self.connection.close()
        return rows
