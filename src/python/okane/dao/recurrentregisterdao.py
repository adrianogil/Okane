

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
                recurrence TEXT,
                recurrence_number INTEGER,
                FOREIGN KEY (id_category) REFERENCES Categories (id_category)
                FOREIGN KEY (id_account) REFERENCES Accounts (id_account)
                PRIMARY KEY (id_recurrent_register)
                )
        ''')
