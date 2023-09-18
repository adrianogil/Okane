import sqlite3
import json
import os

class DbController:
    def __init__(self, okane_directory):
        self.okane_directory = okane_directory

        try:
            self.config_path = os.environ["OKANE_CONFIG_PATH"]
        except:
            self.config_path = self.okane_directory + "/../config/okane.config"
        self.load_config()

        db_folder = os.path.dirname(self.db_path)
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)
        self.conn = sqlite3.connect(self.db_path)

        # Creating cursor
        self.cursor = self.conn.cursor()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)
        else:
            config_data = {
                "db_path" : self.okane_directory + "/../db/okane.sqlite"
            }
            # Writing JSON data
            if not os.path.exists(self.okane_directory + "/../config/"):
                os.mkdir(self.okane_directory + "/../config")
            with open(self.config_path, 'w') as f:
                json.dump(config_data, f)

        self.db_path = config_data['db_path']
