import click
import os
from src.database.importer import SQLImporter
from src.database.connection import DatabaseConnection

@click.group()
def cli():
    """SQL Import Tool - Công cụ import database MySQL"""
    pass

@cli.command()
@click.option('--config', '-c', help='Đường dẫn đến file config')
def test_connection(config):
    """Test kết nối đến database"""
    db = DatabaseConnection(config)
    if db.test_connection():
        click.echo("✓ Kết nối database thành công!")
    else:
        click.echo("✗ Không thể kết nối đến database!")
    db.disconnect()

@cli.command()
@click.argument('sql_file', type=click.Path(exists=True))
@click.option('--config', '-c', help='Đường dẫn đến file config')
@click.option('--no-split', is_flag=True, help='Không chia nhỏ file lớn')
def import_sql(sql_file, config, no_split):
    """Import file SQL vào database"""
    click.echo(f"Đang import file: {sql_file}")

    importer = SQLImporter(config)
    success = importer.import_sql_file(sql_file, split_large_files=not no_split)

    if success:
        click.echo("✓ Import hoàn tất thành công!")
    else:
        click.echo("✗ Import thất bại!")

@cli.command()
@click.argument('sql_file', type=click.Path(exists=True))
@click.option('--output-dir', '-o', default='./chunks', help='Thư mục output cho các file chunks')
@click.option('--max-size', '-s', default=50, type=float, help='Kích thước tối đa cho mỗi chunk (MB)')
def split_file(sql_file, output_dir, max_size):
    """Chia nhỏ file SQL thành nhiều file nhỏ hơn"""
    from src.utils.file_splitter import SQLFileSplitter

    splitter = SQLFileSplitter(max_size)
    chunks = splitter.split_sql_file(sql_file, output_dir)

    click.echo(f"✓ Đã chia thành {len(chunks)} file:")
    for chunk in chunks:
        click.echo(f"  - {chunk}")

@cli.command()
def help():
    """Hiển thị hướng dẫn chi tiết sử dụng"""
    click.echo("🚀 SQL Import Tool - Hướng dẫn sử dụng")
    click.echo("=" * 50)
    click.echo()
    click.echo("1. Test kết nối database:")
    click.echo("   python -m src.main test-connection")
    click.echo()
    click.echo("2. Import file SQL:")
    click.echo("   python -m src.main import-sql my_database.sql")
    click.echo("   python -m src.main import-sql my_database.sql --no-split")
    click.echo()
    click.echo("3. Chia nhỏ file SQL:")
    click.echo("   python -m src.main split-file my_database.sql")
    click.echo("   python -m src.main split-file my_database.sql -s 30 -o ./chunks")
    click.echo()
    click.echo("💡 Tips:")
    click.echo("   - File > 50MB sẽ tự động được chia nhỏ khi import")
    click.echo("   - Sử dụng --no-split để bỏ qua việc chia file")
    click.echo("   - Config database trong config/database.yaml")
    click.echo()

@cli.command()
@click.argument('sql_file', type=click.Path(exists=True))
def info(sql_file):
    """Hiển thị thông tin file SQL"""
    import os
    from src.utils.file_splitter import SQLFileSplitter

    file_size = os.path.getsize(sql_file)
    file_size_mb = file_size / (1024 * 1024)

    click.echo(f"📄 Thông tin file: {sql_file}")
    click.echo("=" * 50)
    click.echo(f"Kích thước: {file_size_mb:.2f} MB ({file_size:,} bytes)")

    # Đếm số dòng
    with open(sql_file, 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)
    click.echo(f"Số dòng: {line_count:,}")

    # Ước tính số chunks nếu chia
    splitter = SQLFileSplitter(50)
    if file_size > splitter.max_size_bytes:
        estimated_chunks = file_size // splitter.max_size_bytes + 1
        click.echo(f"Ước tính số chunks (50MB): {estimated_chunks}")
    else:
        click.echo("File đủ nhỏ, không cần chia")

    # Kiểm tra encoding
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            f.read(100)
        click.echo("Encoding: UTF-8 ✓")
    except UnicodeDecodeError:
        click.echo("Encoding: Không phải UTF-8 ⚠️")

    click.echo()

if __name__ == '__main__':
    cli()