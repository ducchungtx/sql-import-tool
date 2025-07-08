# SQL Import Tool

Công cụ Python để import file SQL vào MySQL database với khả năng tự động chia nhỏ file lớn để tránh timeout.

## Tính năng

- ✅ Kết nối MySQL với cấu hình từ file YAML
- ✅ Tự động chia nhỏ file SQL lớn thành các chunk nhỏ hơn
- ✅ Progress bar hiển thị tiến trình import
- ✅ Xử lý các delimiter tùy chỉnh (DELIMITER ;; etc.)
- ✅ Rollback khi có lỗi
- ✅ Command line interface thân thiện
- ✅ Test kết nối database

## Cài đặt

1. Cài đặt dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Cấu hình

File `config/database.yaml` đã được cấu hình:

```yaml
host: 10.10.8.20
user: root
password: root
database: your_database
port: 3306
```

## Sử dụng

### 1. Test kết nối database

```bash
python -m src.main test-connection
```

### 2. Import file SQL

```bash
# Import với tự động chia nhỏ file (mặc định)
python -m src.main import-sql database/mythaco_staging_v2.sql

# Import không chia nhỏ file
python -m src.main import-sql database/mythaco_staging_v2.sql --no-split

# Sử dụng config file khác
python -m src.main import-sql database/mythaco_staging_v2.sql -c /path/to/config.yaml
```

### 3. Chỉ chia nhỏ file (không import)

```bash
# Chia file thành các chunk 50MB
python -m src.main split-file database/mythaco_staging_v2.sql

# Chia file thành các chunk 30MB, lưu vào thư mục custom
python -m src.main split-file database/mythaco_staging_v2.sql -o ./my_chunks -s 30
```

## Testing

To run the tests, use the following command:

```
pytest tests/
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.