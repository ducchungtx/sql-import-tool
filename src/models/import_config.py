class ImportConfig:
    def __init__(self, sql_file_path, db_host, db_user, db_password, db_name):
        self.sql_file_path = sql_file_path
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name

    def get_connection_details(self):
        return {
            'host': self.db_host,
            'user': self.db_user,
            'password': self.db_password,
            'database': self.db_name
        }