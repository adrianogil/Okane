
class CategoryDAO:
    NO_CATEGORY = 'No Category'

    def __init__(self, db_controller, entityFactory):
        self.conn = db_controller.conn
        self.cursor = db_controller.cursor
        self.entityFactory = entityFactory
        self.noCategory = None

    def createTables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Categories (
                id_category INTEGER,
                category_name TEXT,
                parent_id INTEGER,
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
        parent_category=None
        if row[2] and int(row[2]):
            parent_category = self.getCategoryFromId(int(row[2]))
        category = self.entityFactory.createCategory(
            name=row[1], 
            id=int(row[0]),
            parent=parent_category
        )

        return category
    
    def getChildrenCategories(self, parent_id, recursive=True):
        sql_query_get = "SELECT * from Categories WHERE parent_id = ?"
        sql_data = (parent_id,)
        self.cursor.execute(sql_query_get, sql_data)
        rows = self.cursor.fetchall()

        children_categories = []
        for row in rows:
            category = self.entityFactory.createCategory(
                name=row[1], 
                id=int(row[0]),
                parent=self.getCategoryFromId(int(row[2])) if row[2] else None
            )
            children_categories.append(category)
            if category.parent and recursive:
                children_categories.extend(self.getChildrenCategories(category.id))

        return children_categories

    def getAll(self):
        sql_query_get = "SELECT * from Categories ORDER BY id_category"
        self.cursor.execute(sql_query_get)
        
        category_list = []
        categories_by_id = {}
        parent_by_id = {}

        for row in self.cursor:
            category_data = {
                "id": int(row[0]),
                "name": row[1],
                "parent": row[2]
            }
            category = self.entityFactory.createCategory(**{k: category_data[k] for k in ["id", "name"]})
            categories_by_id[category.id] = category
            parent_by_id[category.id] = category_data["parent"]
            category_list.append(category)
        
        for category_id in parent_by_id:
            target_parent = parent_by_id[category_id]
            if target_parent:
                parent_category = categories_by_id[target_parent]
                categories_by_id[category_id].parent = parent_category    

        return category_list

    def getCategoryFromId(self, id):
        sql_query_get = "SELECT * from Categories WHERE id_category LIKE ?"
        sql_data = (id,)
        self.cursor.execute(sql_query_get, sql_data)
        row = self.cursor.fetchone()
        if row is None:
            return None
        category = self.entityFactory.createCategory(row[1])
        category.id = int(row[0])

        return category

    def saveCategory(self, name, parent_id=None):
        sql_query_save = "INSERT INTO Categories (category_name, parent_id)" + \
                        " VALUES (?, ?)"
        save_data = (name, parent_id)
        self.cursor.execute(sql_query_save, save_data)
        self.conn.commit()

    def updateCategory(self, category):
        sql_query_update = "UPDATE Categories SET category_name = ? WHERE id_category = ?"
        update_data = (category.name, category.id)
        self.cursor.execute(sql_query_update, update_data)
        self.conn.commit()

    def delete(self, category):
        sql_query_delete = "DELETE FROM Categories WHERE id_category = ?"
        delete_data = (category.id,)
        self.cursor.execute(sql_query_delete, delete_data)
        self.conn.commit()

