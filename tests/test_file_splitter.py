import unittest
import tempfile
import os
import shutil
from src.utils.file_splitter import SQLFileSplitter


class TestSQLFileSplitter(unittest.TestCase):
    def setUp(self):
        """Thiết lập trước mỗi test"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test.sql')
        self.output_dir = os.path.join(self.test_dir, 'chunks')

        # Tạo file SQL test
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("-- Test SQL file\n")
            f.write("CREATE DATABASE test_db;\n")
            f.write("USE test_db;\n")
            for i in range(1000):
                f.write(f"INSERT INTO test VALUES ({i}, 'data_{i}');\n")

    def tearDown(self):
        """Dọn dẹp sau mỗi test"""
        shutil.rmtree(self.test_dir)

    def test_split_small_file(self):
        """Test file nhỏ không cần chia"""
        splitter = SQLFileSplitter(max_size_mb=10)  # 10MB
        result = splitter.split_sql_file(self.test_file, self.output_dir)

        # File nhỏ sẽ trả về chính nó
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.test_file)

    def test_split_large_file(self):
        """Test chia file lớn"""
        # Tạo file lớn
        large_file = os.path.join(self.test_dir, 'large.sql')
        with open(large_file, 'w', encoding='utf-8') as f:
            for i in range(10000):
                f.write(f"INSERT INTO large_table VALUES ({i}, '{'A' * 100}');\n")

        splitter = SQLFileSplitter(max_size_mb=0.5)  # 0.5MB
        result = splitter.split_sql_file(large_file, self.output_dir)

        # Phải có nhiều hơn 1 chunk
        self.assertGreater(len(result), 1)

        # Kiểm tra tất cả file chunks tồn tại
        for chunk_file in result:
            self.assertTrue(os.path.exists(chunk_file))

    def test_sql_integrity(self):
        """Test tính toàn vẹn của SQL sau khi chia"""
        # Tạo file có stored procedure với delimiter
        sql_content = """-- Test file with delimiter
CREATE DATABASE test_db;
USE test_db;

CREATE TABLE users (id INT, name VARCHAR(100));

DELIMITER ;;
CREATE PROCEDURE GetUsers()
BEGIN
    SELECT * FROM users;
END;;
DELIMITER ;

INSERT INTO users VALUES (1, 'John');
INSERT INTO users VALUES (2, 'Jane');
"""

        test_file = os.path.join(self.test_dir, 'delimiter_test.sql')
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(sql_content)

        splitter = SQLFileSplitter(max_size_mb=0.001)  # Rất nhỏ để buộc chia
        result = splitter.split_sql_file(test_file, self.output_dir)

        # Kiểm tra nội dung được chia đúng
        total_content = ""
        for chunk_file in result:
            with open(chunk_file, 'r', encoding='utf-8') as f:
                total_content += f.read()

        # Nội dung sau khi ghép lại phải giống nội dung gốc
        with open(test_file, 'r', encoding='utf-8') as f:
            original_content = f.read()

        self.assertEqual(total_content.strip(), original_content.strip())


if __name__ == '__main__':
    unittest.main()