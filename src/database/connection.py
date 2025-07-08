import pymysql
from ..utils.config import Config

class DatabaseConnection:
    def __init__(self, config_path=None):
        self.config = Config(config_path)
        self.connection = None

    def connect(self):
        """Kết nối đến MySQL database"""
        try:
            db_config = self.config.get_db_config()
            self.connection = pymysql.connect(**db_config)
            print(f"Đã kết nối thành công đến {db_config['host']}:{db_config['port']}")
            return True
        except Exception as e:
            print(f"Lỗi kết nối database: {e}")
            return False

    def disconnect(self):
        """Ngắt kết nối database"""
        if self.connection:
            self.connection.close()
            print("Đã ngắt kết nối database")

    def execute_query(self, query):
        """Thực thi một câu SQL"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
                return True
        except Exception as e:
            print(f"Lỗi thực thi query: {e}")
            self.connection.rollback()
            return False

    def test_connection(self):
        """Test kết nối database"""
        if self.connect():
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT VERSION()")
                    version = cursor.fetchone()
                    print(f"MySQL version: {version[0]}")
                return True
            except Exception as e:
                print(f"Lỗi test connection: {e}")
                return False
        return False

    def disconnect(self):
        if self.connection:
            self.connection.close()