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

    def getAll(self):
        sql_query_get = "SELECT * from FinancialRegisters ORDER BY date(register_dt)"
        self.cursor.execute(sql_query_get)
        register_list = []
        for row in self.cursor:
            moneyRegister = self.entityFactory.createMoneyRegister({})
            moneyRegister.id = int(row[0])
            moneyRegister.register_dt = dtparse(str(row[3]))
            moneyRegister.amount = int(row[2])
            moneyRegister.description = str(row[1])
            moneyRegister.category = self.categoryDAO.getCategoryFromId(int(row[4]))

            register_list.append(moneyRegister)

        return register_list