from okane.utils.dateutils import get_date as dtparse

import datetime


class MoneyRegisterDAO:
    def __init__(self, db_controller, entityFactory, categoryDAO, accountDAO):
        self.conn = db_controller.conn
        self.cursor = db_controller.cursor
        self.entityFactory = entityFactory
        self.categoryDAO = categoryDAO
        self.accountDAO = accountDAO

    def createTables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS FinancialRegisters (
                id_register INTEGER PRIMARY KEY,
                description TEXT,
                amount REAL,
                register_dt TEXT,
                id_category INTEGER,
                id_account INTEGER,
                confirmed BOOLEAN,
                id_recurrent_register INTEGER,
                FOREIGN KEY (id_category) REFERENCES Categories (id_category),
                FOREIGN KEY (id_account) REFERENCES Accounts (id_account),
                FOREIGN KEY (id_recurrent_register) REFERENCES FinancialRecurrentRegisters (id_recurrent_register)
            )
        ''')

    def save(self, moneyRegister, force_id=None):
        # Save current register
        sql_query_save = "INSERT INTO FinancialRegisters (description, amount, register_dt, id_category, id_account, confirmed, id_recurrent_register)" + \
                        " VALUES (:description,:amount,:register_dt,:id_category,:id_account,:confirmed,:id_recurrent_register)"
        save_data = moneyRegister.get_data_tuple() + (moneyRegister.recurrent_register.id if moneyRegister.recurrent_register else None,)
        if force_id is not None:
            # Force id to be used (in case register info is loaded from a file)
            sql_query_save = "INSERT INTO FinancialRegisters (id_register, description, amount, register_dt, id_category, id_account, confirmed, id_recurrent_register)" + \
                        " VALUES (:id_register, :description,:amount,:register_dt,:id_category,:id_account,:confirmed,:id_recurrent_register)"
            save_data = (force_id,) + save_data
        # print(str(save_data))
        self.cursor.execute(sql_query_save, save_data)
        self.conn.commit()

        return self.cursor.lastrowid

    def update(self, moneyRegister):
        sql_query_update = "UPDATE FinancialRegisters SET description = ?," + \
                                                             " amount = ?," + \
                                                        " register_dt = ?," + \
                                                        " id_category = ?, " + \
                                                        " id_account  = ?, " + \
                                                        " confirmed  = ? " + \
                                            " WHERE id_register = ?"
        update_data = moneyRegister.get_data_tuple() + (moneyRegister.id,)
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

    def getAll(self, extra_args=None):
        # print(extra_args)
        if extra_args is None:
            extra_args = {
                '-l': []
            }

        sql_query_get = "SELECT * from FinancialRegisters "
        order_by = " ORDER BY date(register_dt)"
        conditions_data = ()
        conditions = ''
        if '-i' in extra_args:
            conditions = self.addToConditions(conditions, "amount >= 0")
            # print('Debug: moneyregisterdao - added since ' + dt)
        elif '-o' in extra_args:
            conditions = self.addToConditions(conditions, "amount < 0")
            # print('Debug: moneyregisterdao - added since ' + dt)
        if '-dt' in extra_args:
            conditions = self.addToConditions(conditions, "register_dt LIKE ?")
            dt = dtparse(extra_args['-dt'][0]).strftime("%Y-%m-%d")
            conditions_data = conditions_data + (dt + "%" ,)
        if '-today' in extra_args:
            conditions = self.addToConditions(conditions, "register_dt LIKE ?")
            dt = datetime.datetime.now().strftime("%Y-%m-%d")
            conditions_data = conditions_data + (dt + "%" ,)
        if '-since' in extra_args:
            conditions = self.addToConditions(conditions, "date(register_dt) >= date( ? )")
            dt = dtparse(extra_args['-since'][0]).strftime("%Y-%m-%d")
            conditions_data = conditions_data + (dt,)
            # print('Debug: moneyregisterdao - added since ' + dt)
        if '-until' in extra_args:
            conditions = self.addToConditions(conditions, "date(register_dt) <= date( ? )")
            dt = dtparse(extra_args['-until'][0]).strftime("%Y-%m-%d")
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
        if 'accounts' in extra_args:
            account_conditions = ''
            for c in extra_args['accounts']:
                if account_conditions == '':
                    account_conditions = 'id_account = ?'
                else:
                    account_conditions = account_conditions + 'OR id_account = ?'
                conditions_data = conditions_data + (c.id,)
            account_conditions = '(' + account_conditions + ')'
            conditions = self.addToConditions(conditions, account_conditions)
        if 'description' in extra_args:
            description_condition = 'description LIKE ?'
            conditions_data = conditions_data + ('%' + extra_args['description'] + '%',)
            conditions = self.addToConditions(conditions, description_condition)
        if 'limit' in extra_args:
            order_by = order_by + " LIMIT " + extra_args['limit'] + " "
        if 'offset' in extra_args:
            order_by = order_by + " OFFSET " + extra_args['offset'] + " "
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
        moneyRegister.amount = float(row[2])
        moneyRegister.description = row[1]
        moneyRegister.category = self.categoryDAO.getCategoryFromId(int(row[4]))
        moneyRegister.account = self.accountDAO.getAccountFromId(int(row[5]))

        return moneyRegister

    def load_all_registers_into_dataframe(self, extra_args=None):
        import pandas as pd
        # Get all money registers using the existing getAll method
        register_list = self.getAll(extra_args)

        # Convert each MoneyRegister object to a dictionary
        data = [register.get_data() for register in register_list]

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data)

        return df
