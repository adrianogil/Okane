
class MoneyRegisterDAO:
    def __init__(self, cursor):
        self.cursor = cursor

    def createTables(self):
        c.execute('''
        CREATE TABLE IF NOT EXISTS FinancialRegisters (
            id_register INTEGER,
            description TEXT,
            amount REAL,
            register_dt TEXT,
            PRIMARY KEY (id_register)
            )
        ''')