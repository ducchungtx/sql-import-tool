import unittest
import tempfile
import os
import shutil
from unittest.mock import Mock, patch, MagicMock
from src.database.importer import SQLImporter


class TestSQLImporter(unittest.TestCase):
    def setUp(self):
        """Thiết lập trước mỗi test"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test.sql')

        # Tạo file SQL test
        sql_content = """-- Test SQL file
CREATE DATABASE IF NOT EXISTS test_db;
USE test_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);

INSERT INTO users (name, email) VALUES ('John', 'john@test.com');
INSERT INTO users (name, email) VALUES ('Jane', 'jane@test.com');

SELECT COUNT(*) FROM users;
"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(sql_content)

    def tearDown(self):
        """Dọn dẹp sau mỗi test"""
        shutil.rmtree(self.test_dir)

    @patch('src.database.importer.DatabaseConnection')
    def test_import_file_not_exists(self, mock_db_connection):
        """Test import file không tồn tại"""
        importer = SQLImporter()
        result = importer.import_sql_file('/path/does/not/exist.sql')
        self.assertFalse(result)

    @patch('src.database.importer.DatabaseConnection')
    def test_import_connection_failed(self, mock_db_connection):
        """Test import khi kết nối database thất bại"""
        # Mock database connection fail
        mock_db = Mock()
        mock_db.connect.return_value = False
        mock_db_connection.return_value = mock_db

        importer = SQLImporter()
        result = importer.import_sql_file(self.test_file)

        self.assertFalse(result)
        mock_db.connect.assert_called_once()

    @patch('src.database.importer.DatabaseConnection')
    def test_import_small_file_success(self, mock_db_connection):
        """Test import file nhỏ thành công"""
        # Mock database connection success
        mock_db = Mock()
        mock_db.connect.return_value = True
        mock_db.execute_query.return_value = True
        mock_db_connection.return_value = mock_db

        importer = SQLImporter()
        result = importer.import_sql_file(self.test_file, split_large_files=False)

        self.assertTrue(result)
        mock_db.connect.assert_called_once()
        mock_db.disconnect.assert_called_once()


if __name__ == '__main__':
    unittest.main()