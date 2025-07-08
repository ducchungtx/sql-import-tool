import os
import time
from tqdm import tqdm
from .connection import DatabaseConnection
from ..utils.file_splitter import SQLFileSplitter

class SQLImporter:
    def __init__(self, config_path=None):
        self.db = DatabaseConnection(config_path)
        self.splitter = SQLFileSplitter()

    def import_sql_file(self, sql_file_path, split_large_files=True):
        """Import file SQL vào database"""
        if not os.path.exists(sql_file_path):
            print(f"File không tồn tại: {sql_file_path}")
            return False

        if not self.db.connect():
            return False

        try:
            files_to_import = [sql_file_path]

            # Chia nhỏ file nếu cần
            if split_large_files:
                file_size = os.path.getsize(sql_file_path)
                if file_size > 50 * 1024 * 1024:  # > 50MB
                    print("File lớn, đang chia nhỏ...")
                    output_dir = os.path.join(os.path.dirname(sql_file_path), 'chunks')
                    files_to_import = self.splitter.split_sql_file(sql_file_path, output_dir)

            # Import từng file
            total_success = 0
            for i, file_path in enumerate(files_to_import):
                print(f"\nĐang import file {i+1}/{len(files_to_import)}: {os.path.basename(file_path)}")
                if self._import_single_file(file_path):
                    total_success += 1
                    print(f"✓ Import thành công: {os.path.basename(file_path)}")
                else:
                    print(f"✗ Import thất bại: {os.path.basename(file_path)}")

            print(f"\nKết quả: {total_success}/{len(files_to_import)} file được import thành công")
            return total_success == len(files_to_import)

        except Exception as e:
            print(f"Lỗi trong quá trình import: {e}")
            return False
        finally:
            self.db.disconnect()

    def _import_single_file(self, file_path):
        """Import một file SQL đơn lẻ"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Tách các câu SQL
            statements = self._split_sql_statements(content)

            success_count = 0
            with tqdm(total=len(statements), desc="Executing SQL") as pbar:
                for statement in statements:
                    if statement.strip():
                        if self.db.execute_query(statement):
                            success_count += 1
                        time.sleep(0.01)  # Tránh overload
                    pbar.update(1)

            print(f"Đã thực thi {success_count}/{len(statements)} câu SQL")
            return success_count == len(statements)

        except Exception as e:
            print(f"Lỗi đọc file {file_path}: {e}")
            return False

    def _split_sql_statements(self, content):
        """Tách nội dung SQL thành các câu lệnh riêng biệt"""
        # Xử lý delimiter
        statements = []
        current_delimiter = ';'

        lines = content.split('\n')
        current_statement = []

        for line in lines:
            line = line.strip()

            # Bỏ qua comment và dòng trống
            if not line or line.startswith('--') or line.startswith('#'):
                continue

            # Xử lý DELIMITER
            if line.upper().startswith('DELIMITER'):
                if current_statement:
                    statements.append('\n'.join(current_statement))
                    current_statement = []
                current_delimiter = line.split()[1]
                continue

            current_statement.append(line)

            # Kiểm tra kết thúc statement
            if line.endswith(current_delimiter):
                if current_delimiter != ';':
                    # Loại bỏ delimiter tùy chỉnh
                    current_statement[-1] = line[:-len(current_delimiter)].strip()
                statements.append('\n'.join(current_statement))
                current_statement = []

        # Thêm statement cuối cùng nếu có
        if current_statement:
            statements.append('\n'.join(current_statement))

        return statements