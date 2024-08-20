

class MoneyRecurrentRegisterDAO:
    def __init__(self, db_controller, entityFactory, categoryDAO, accountDAO):
        self.conn = db_controller.conn
        self.cursor = db_controller.cursor
        self.entityFactory = entityFactory
        self.categoryDAO = categoryDAO
        self.accountDAO = accountDAO


    def createTables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS FinancialRecurrentRegisters (
                id_recurrent_register INTEGER,
                description TEXT,
                amount REAL,
                start_dt TEXT,
                end_dt TEXT,
                id_category INTEGER,
                id_account INTEGER,
                recurrence TEXT CHECK(recurrence IN ('daily', 'weekly', 'monthly', 'yearly', 'custom')),
                recurrence_number INTEGER,
                FOREIGN KEY (id_category) REFERENCES Categories (id_category),
                FOREIGN KEY (id_account) REFERENCES Accounts (id_account),
                PRIMARY KEY (id_recurrent_register)
            )
        ''')

    def save(self, moneyRecurrentRegister):
        # Save current register
        sql_query_save = "INSERT INTO FinancialRecurrentRegisters (description, amount, start_dt, end_dt, id_category, id_account, recurrence, recurrence_number)" + \
                        " VALUES (:description,:amount,:start_dt,:end_dt,:id_category,:id_account,:recurrence,:recurrence_number)"
        save_data = moneyRecurrentRegister.get_data_tuple()
        self.cursor.execute(sql_query_save, save_data)
        self.conn.commit()

        return self.cursor.lastrowid

    def update(self, moneyRecurrentRegister):
        sql_query_update = "UPDATE FinancialRecurrentRegisters SET description = ?," + \
                                                             " amount = ?," + \
                                                        " start_dt = ?," + \
                                                        " end_dt = ?," + \
                                                        " id_category = ?, " + \
                                                        " id_account  = ?, " + \
                                                        " recurrence  = ?, " + \
                                                        " recurrence_number  = ? " + \
                                            " WHERE id_recurrent_register = ?"
        update_data = moneyRecurrentRegister.get_data_tuple() + (moneyRecurrentRegister.id,)
        self.cursor.execute(sql_query_update, update_data)
        self.conn.commit()

    def delete(self, moneyRecurrentRegister):
        sql_query_delete = "DELETE FROM FinancialRecurrentRegisters WHERE id_recurrent_register=?"
        delete_data = (moneyRecurrentRegister.id,)
        self.cursor.execute(sql_query_delete, delete_data)
        self.conn.commit()

    def getFromId(self, id):
        sql_query_get = "SELECT * from FinancialRecurrentRegisters WHERE id_recurrent_register = ?"
        get_data = (id,)

        self.cursor.execute(sql_query_get, get_data)
        row = self.cursor.fetchone()
        return self.entityFactory.createMoneyRecurrentRegister(row)

    def getFromIdList(self, id_list):
        sql_query_get = "SELECT * from FinancialRecurrentRegisters WHERE id_recurrent_register IN ({})".format(','.join('?' * len(id_list)))
        get_data = id_list

        self.cursor.execute(sql_query_get, get_data)
        rows = self.cursor.fetchall()
        return [self.entityFactory.createMoneyRecurrentRegister(row) for row in rows]
