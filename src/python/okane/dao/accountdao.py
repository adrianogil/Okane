
class AccountDAO:
    DEFAULT_Account = 'In Cash'

    def __init__(self, db_controller, entityFactory):
        self.conn = db_controller.conn
        self.cursor = db_controller.cursor
        self.entityFactory = entityFactory
        self.noCategory = None

    def createTables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Accounts (
                id_account INTEGER,
                account_name TEXT,
                PRIMARY KEY (id_account)
            )
        ''')
        self.defaultAccount = self.getAccount(AccountDAO.DEFAULT_Account)
        if self.defaultAccount is None:
            print("Creating an 'IN CASH' account")
            self.saveAccount(AccountDAO.DEFAULT_Account)
            self.defaultAccount = self.getAccount(AccountDAO.DEFAULT_Account)
        # print('No Category with id: ' + str(self.noCategory.id))

    def getAccount(self, name):
        # print('DEBUG: categoryDAO - trying to get category from name: ' + name)
        sql_query_get = "SELECT * from Accounts WHERE account_name LIKE ?"
        sql_data = (name,)
        self.cursor.execute(sql_query_get, sql_data)
        row = self.cursor.fetchone()
        if row is None:
            return None
        account = self.entityFactory.createAccount(str(row[1]))
        account.id = int(row[0])

        return account

    def getAll(self):
        sql_query_get = "SELECT * from Accounts ORDER BY id_account"
        self.cursor.execute(sql_query_get)
        account_list = []
        for row in self.cursor:
            account = self.entityFactory.createAccount(str(row[1]))
            account.id = int(row[0])

            account_list.append(account)

        return account_list

    def getAccountFromId(self, id):
        sql_query_get = "SELECT * from Accounts WHERE id_account LIKE ?"
        sql_data = (id,)
        self.cursor.execute(sql_query_get, sql_data)
        row = self.cursor.fetchone()
        if row is None:
            return None
        account = self.entityFactory.createAccount(str(row[1]))
        account.id = int(row[0])

        return account

    def saveAccount(self, name):
        sql_query_save = "INSERT INTO Accounts (account_name)" + \
                        " VALUES (:account_name)"
        save_data = (name, )
        self.cursor.execute(sql_query_save, save_data)
        self.conn.commit()

    def update(self, account):
        sql_query_update = "UPDATE Accounts SET account_name = ? WHERE id_account = ?"
        update_data = (account.name, account.id)
        self.cursor.execute(sql_query_update, update_data)
        self.conn.commit()

    def delete(self, account):
        sql_query_delete = "DELETE FROM Accounts WHERE id_account = ?"
        delete_data = (account.id,)
        self.cursor.execute(sql_query_delete, delete_data)
        self.conn.commit()

