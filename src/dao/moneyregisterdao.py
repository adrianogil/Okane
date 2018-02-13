
class MoneyRegisterDAO:
    def __init__(self, conn, cursor, entityFactory):
        self.conn = conn
        self.cursor = cursor
        self.entityFactory = entityFactory

    def createTables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS FinancialRegisters (
            id_register INTEGER,
            description TEXT,
            amount REAL,
            register_dt TEXT,
            PRIMARY KEY (id_register)
            )
        ''')

    def save(self, moneyRegister):
        # Save current register
        sql_query_save = "INSERT INTO FinancialRegisters (description, amount, register_dt)" + \
                        " VALUES (:description,:amount,:register_dt)"
        save_data = (moneyRegister.description, \
                     moneyRegister.amount, \
                     moneyRegister.get_register_dt()) # YYYY-MM-DD HH:MM:SS.SSS
        self.cursor.execute(sql_query_save, save_data)
        self.conn.commit()