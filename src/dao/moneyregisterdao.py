from dateutil.parser import parse as dtparse

class MoneyRegisterDAO:
    def __init__(self, conn, cursor, entityFactory, categoryDAO):
        self.conn = conn
        self.cursor = cursor
        self.entityFactory = entityFactory
        self.categoryDAO = categoryDAO

    def createTables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS FinancialRegisters (
                id_register INTEGER,
                description TEXT,
                amount REAL,
                register_dt TEXT,
                id_category INTEGER,
                FOREIGN KEY (id_category) REFERENCES Categories (id_category)
                PRIMARY KEY (id_register)
                )
        ''')

    def save(self, moneyRegister):
        # Save current register
        sql_query_save = "INSERT INTO FinancialRegisters (description, amount, register_dt, id_category)" + \
                        " VALUES (:description,:amount,:register_dt,:id_category)"
        save_data = (moneyRegister.description, \
                     moneyRegister.amount, \
                     moneyRegister.get_register_dt(),\
                     moneyRegister.category.id) # YYYY-MM-DD HH:MM:SS.SSS
        self.cursor.execute(sql_query_save, save_data)
        self.conn.commit()

    def update(self, moneyRegister):
        sql_query_update = "UPDATE FinancialRegisters SET description = ?," + \
                                                             " amount = ?," + \
                                                        " register_dt = ?," + \
                                                        " id_category = ? " + \
                                              " WHERE id_register = ?"
        update_data = (moneyRegister.description, \
                       moneyRegister.amount, \
                       moneyRegister.get_register_dt(),\
                       moneyRegister.category.id,\
                       moneyRegister.id)
        self.cursor.execute(sql_query_update, update_data)
        self.conn.commit()

    def delete(self, moneyRegister):
        sql_query_delete = "DELETE FROM FinancialRegisters WHERE id_register=?"
        delete_data = (moneyRegister.id,)
        self.cursor.execute(sql_query_delete, delete_data)
        self.conn.commit()

    def getFromId(self, id):
        sql_query_get = "SELECT * from FinancialRegisters WHERE id_register = ?"
        get_data = (id,)
        self.cursor.execute(sql_query_get, get_data)
        row = self.cursor.fetchone()
        if row is None:
            return None
        moneyRegister = self.entityFactory.createMoneyRegister({})
        moneyRegister.id = int(row[0])
        moneyRegister.register_dt = dtparse(str(row[3]))
        moneyRegister.amount = int(row[2])
        moneyRegister.description = str(row[1])
        moneyRegister.category = self.categoryDAO.getCategoryFromId(int(row[4]))

        return moneyRegister

    def getAll(self):
        sql_query_get = "SELECT * from FinancialRegisters ORDER BY date(register_dt)"
        # print('Debug: moneyregisterdao.getAll - sql_query_get: ' + sql_query_get)
        self.cursor.execute(sql_query_get)
        rows = self.cursor.fetchall()
        # print('Debug: moneyregisterdao.getAll - found ' + str(len(rows)) + ' entries')
        register_list = []
        for row in rows:
            # print('Debug: moneyregisterdao.getAll - parse register')
            moneyRegister = self.entityFactory.createMoneyRegister({})
            moneyRegister.id = int(row[0])
            moneyRegister.register_dt = dtparse(str(row[3]))
            moneyRegister.amount = int(row[2])
            moneyRegister.description = str(row[1])
            moneyRegister.category = self.categoryDAO.getCategoryFromId(int(row[4]))

            register_list.append(moneyRegister)

        return register_list