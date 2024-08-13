from okane.dao.moneyregisterdao import MoneyRegisterDAO
from okane.dao.categorydao import CategoryDAO
from okane.dao.accountdao import AccountDAO
from okane.entity.entityfactory import EntityFactory

import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

import os


class CategorySuggestionController:
    def __init__(self, db_controller):
        self.db_controller = db_controller
        self.entityFactory = EntityFactory()
        self.accountDAO = AccountDAO(self.db_controller, self.entityFactory)
        self.categoryDAO = CategoryDAO(self.db_controller, self.entityFactory)
        self.moneyDAO = MoneyRegisterDAO(self.db_controller, self.entityFactory, \
                self.categoryDAO, self.accountDAO)
        self.model = None
        self.vectorizer = None

        self.model_path = os.path.join(
            db_controller.okane_directory,
            'expense_category_model.pkl'
        )
        self.vectorizer_path = os.path.join(
            db_controller.okane_directory,
            'vectorizer.pkl'
        )

    def load_model(self):
        try:
            with open(self.model_path, 'rb') as model_file:
                self.model = pickle.load(model_file)
            with open(self.vectorizer_path, 'rb') as vectorizer_file:
                self.vectorizer = pickle.load(vectorizer_file)
        except FileNotFoundError:
            print("Model not found. Try to train a new model.")

    def train_model(self):
        print("Starting model training...")

        print("Loading data...")
        data = self.moneyDAO.getAll()

        print(f"Loaded {len(data)} registers.")
        descriptions = [row.description for row in data]
        categories = [row.category.name for row in data]

        print("Training model...")
        self.vectorizer = CountVectorizer()
        X = self.vectorizer.fit_transform(descriptions)
        y = categories

        self.model = RandomForestClassifier()
        self.model.fit(X, y)

        with open(self.model_path, 'wb') as model_file:
            pickle.dump(self.model, model_file)
        with open(self.vectorizer_path, 'wb') as vectorizer_file:
            pickle.dump(self.vectorizer, vectorizer_file)

    def suggest_category(self, description):
        if not self.model or not self.vectorizer:
            self.train_model()
        X_new = self.vectorizer.transform([description])
        predicted_category = self.model.predict(X_new)
        return str(predicted_category[0])

if __name__ == '__main__':
    from okane.dbcontroller import DbController
    from pyutils.utils.userinput import get_user_input

    okane_directory = os.environ.get('OKANE_DIR', '')
    db_controller = DbController(okane_directory)
    category_suggestion_controller = CategorySuggestionController(db_controller)

    user_answer = get_user_input("Do you want to train a new model? (y/n)")
    if user_answer == 'y':
        category_suggestion_controller.train_model()
    else:
        print("Let's test the model!")
        category_suggestion_controller.load_model()
        while True:
            description = get_user_input("Enter a description: ")
            category = category_suggestion_controller.suggest_category(description)
            print(f"Predicted category: {category}")
            user_answer = get_user_input("Do you want to continue? (y/n)")
            if user_answer == 'n':
                break

