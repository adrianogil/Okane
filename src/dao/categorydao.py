
class CategoryDAO:
    NO_CATEGORY = 'No Category'

    def __init__(self, conn, cursor, entityFactory):
        self.conn = conn
        self.cursor = cursor
        self.entityFactory = entityFactory
        self.noCategory = None

    def createTables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Categories (
                id_category INTEGER,
                category_name TEXT,
                PRIMARY KEY (id_category)
            )
        ''')
        self.noCategory = self.getCategory(CategoryDAO.NO_CATEGORY)
        if self.noCategory is None:
            self.saveCategory(CategoryDAO.NO_CATEGORY)
            self.noCategory = self.getCategory(CategoryDAO.NO_CATEGORY)
        # print('No Category with id: ' + str(self.noCategory.id))

    def getCategory(self, name):
        # print('DEBUG: categoryDAO - trying to get category from name: ' + name)
        sql_query_get = "SELECT * from Categories WHERE category_name LIKE ?"
        sql_data = (name,)
        self.cursor.execute(sql_query_get, sql_data)
        row = self.cursor.fetchone()
        if row is None:
            return None
        category = self.entityFactory.createCategory(str(row[1]))
        category.id = int(row[0])

        return category

    def getCategoryFromId(self, id):
        sql_query_get = "SELECT * from Categories WHERE id_category LIKE ?"
        sql_data = (id,)
        self.cursor.execute(sql_query_get, sql_data)
        row = self.cursor.fetchone()
        if row is None:
            return None
        category = self.entityFactory.createCategory(str(row[1]))
        category.id = int(row[0])

        return category

    def saveCategory(self, name):
        sql_query_save = "INSERT INTO Categories (category_name)" + \
                        " VALUES (:category_name)"
        save_data = (name, )
        self.cursor.execute(sql_query_save, save_data)
        self.conn.commit()
        