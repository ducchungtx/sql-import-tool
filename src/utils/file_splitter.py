import os
import re
from tqdm import tqdm

class SQLFileSplitter:
    def __init__(self, max_size_mb=50):
        self.max_size_bytes = max_size_mb * 1024 * 1024

    def split_sql_file(self, input_file, output_dir):
        """Chia nhỏ file SQL thành nhiều file nhỏ hơn"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_size = os.path.getsize(input_file)
        print(f"Kích thước file gốc: {file_size / (1024*1024):.2f} MB")

        if file_size <= self.max_size_bytes:
            print("File đã đủ nhỏ, không cần chia.")
            return [input_file]

        split_files = []
        current_file_index = 1
        current_size = 0
        current_content = []

        with open(input_file, 'r', encoding='utf-8') as f:
            total_lines = sum(1 for _ in f)
            f.seek(0)

            with tqdm(total=total_lines, desc="Đang chia file") as pbar:
                for line in f:
                    current_content.append(line)
                    current_size += len(line.encode('utf-8'))
                    pbar.update(1)

                    # Kiểm tra nếu gặp delimiter và đã đạt kích thước tối đa
                    if (current_size >= self.max_size_bytes and
                        (line.strip().endswith(';') or
                         line.strip().upper() in ['DELIMITER ;;', 'DELIMITER ;'])):

                        # Ghi file chunk
                        output_file = os.path.join(output_dir, f"chunk_{current_file_index:03d}.sql")
                        with open(output_file, 'w', encoding='utf-8') as chunk_file:
                            chunk_file.writelines(current_content)

                        split_files.append(output_file)
                        print(f"Đã tạo: {output_file} ({current_size / (1024*1024):.2f} MB)")

                        # Reset cho chunk tiếp theo
                        current_file_index += 1
                        current_size = 0
                        current_content = []

                # Ghi phần còn lại
                if current_content:
                    output_file = os.path.join(output_dir, f"chunk_{current_file_index:03d}.sql")
                    with open(output_file, 'w', encoding='utf-8') as chunk_file:
                        chunk_file.writelines(current_content)
                    split_files.append(output_file)
                    print(f"Đã tạo: {output_file} ({current_size / (1024*1024):.2f} MB)")

        return split_files