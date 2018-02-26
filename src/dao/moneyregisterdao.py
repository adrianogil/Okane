from dateutil.parser import parse as dtparse

class MoneyRegisterDAO:
    def __init__(self, conn, cursor, entityFactory, categoryDAO, accountDAO):
        self.conn = conn
        self.cursor = cursor
        self.entityFactory = entityFactory
        self.categoryDAO = categoryDAO
        self.accountDAO = accountDAO

    def createTables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS FinancialRegisters (
                id_register INTEGER,
                description TEXT,
                amount REAL,
                register_dt TEXT,
                id_category INTEGER,
                id_account INTEGER,
                FOREIGN KEY (id_category) REFERENCES Categories (id_category)
                FOREIGN KEY (id_account) REFERENCES Accounts (id_account)
                PRIMARY KEY (id_register)
                )
        ''')

    def save(self, moneyRegister):
        # Save current register
        sql_query_save = "INSERT INTO FinancialRegisters (description, amount, register_dt, id_category, id_account)" + \
                        " VALUES (:description,:amount,:register_dt,:id_category,:id_account)"
        save_data = moneyRegister.get_data_tuple()
        print(str(save_data))
        self.cursor.execute(sql_query_save, save_data)
        self.conn.commit()

    def update(self, moneyRegister):
        sql_query_update = "UPDATE FinancialRegisters SET description = ?," + \
                                                             " amount = ?," + \
                                                        " register_dt = ?," + \
                                                        " id_category = ? " + \
                                                        " id_account = ? " + \
                                              " WHERE id_register = ?"
        update_data = moneyRegister.get_data_tuple()
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
        moneyRegister = self.parseRegisterFromRow(row)

        return moneyRegister

    def addToConditions(self, conditions, added_term):
        if conditions == '':
            return 'WHERE ' + added_term
        else:
            return conditions + ' AND ' + added_term

    def getAll(self, extra_args):
        sql_query_get = "SELECT * from FinancialRegisters "
        order_by = " ORDER BY date(register_dt)"
        conditions_data = ()
        conditions = ''
        if '-since' in extra_args:
            conditions = self.addToConditions(conditions, "date(register_dt) > date( ? )")
            dt = dtparse(extra_args['-since'][0]).strftime("%Y-%m-%d %H:%M:%S")
            conditions_data = conditions_data + (dt,)
            # print('Debug: moneyregisterdao - added since ' + dt)
        if '-until' in extra_args:
            conditions = self.addToConditions(conditions, "date(register_dt) < date( ? )")
            dt = dtparse(extra_args['-until'][0]).strftime("%Y-%m-%d %H:%M:%S")
            conditions_data = conditions_data + (dt,)
        if 'categories' in extra_args:
            category_conditions = ''
            for c in extra_args['categories']:
                if category_conditions == '':
                    category_conditions = 'id_category = ?'
                else:
                    category_conditions = category_conditions + 'OR id_category = ?'
                conditions_data = conditions_data + (c.id,)
            category_conditions = '(' + category_conditions + ')'
            conditions = self.addToConditions(conditions, category_conditions)
        # print('Debug: moneyregisterdao.getAll - sql_query_get: ' + (sql_query_get + conditions))
        if conditions == '':
            self.cursor.execute(sql_query_get + order_by)
        else:
            # print('Debug: moneyregisterdao.getAll ' + (sql_query_get + conditions))
            self.cursor.execute(sql_query_get + conditions + order_by, conditions_data)
        rows = self.cursor.fetchall()
        # print('Debug: moneyregisterdao.getAll - found ' + str(len(rows)) + ' entries')
        register_list = []
        for row in rows:
            # print('Debug: moneyregisterdao.getAll - parse register')
            moneyRegister = self.parseRegisterFromRow(row)

            register_list.append(moneyRegister)

        return register_list

    def parseRegisterFromRow(self, row):
        moneyRegister = self.entityFactory.createMoneyRegister({})
        moneyRegister.id = int(row[0])
        moneyRegister.register_dt = dtparse(str(row[3]))
        moneyRegister.amount = int(row[2])
        moneyRegister.description = row[1]
        moneyRegister.category = self.categoryDAO.getCategoryFromId(int(row[4]))
        moneyRegister.account = self.accountDAO.getAccountFromId(int(row[5]))

        return moneyRegister