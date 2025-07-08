import yaml
import os

class Config:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'database.yaml')

        with open(config_path, 'r', encoding='utf-8') as file:
            self.config = yaml.safe_load(file)

    def get_db_config(self):
        return {
            'host': self.config.get('host', 'localhost'),
            'user': self.config.get('user', 'root'),
            'password': self.config.get('password', ''),
            'database': self.config.get('database', ''),
            'port': self.config.get('port', 3306),
            'charset': 'utf8mb4'
        }

def load_config(config_file_path):
    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config