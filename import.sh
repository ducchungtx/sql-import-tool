#!/bin/bash

# Màu sắc cho output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Hàm hiển thị help
show_help() {
    echo -e "${BLUE}🚀 SQL Import Tool - Quick Import${NC}"
    echo "=================================="
    echo
    echo "Cách sử dụng:"
    echo "  ./import.sh <file.sql>                    # Import với tự động chia file"
    echo "  ./import.sh <file.sql> --no-split        # Import không chia file"
    echo "  ./import.sh <file.sql> --info             # Chỉ xem thông tin file"
    echo "  ./import.sh <file.sql> --split-only      # Chỉ chia file, không import"
    echo
    echo "Ví dụ:"
    echo "  ./import.sh database/mydatabase.sql"
    echo "  ./import.sh large_file.sql --no-split"
    echo "  ./import.sh huge_file.sql --info"
    echo
}

# Kiểm tra tham số
if [ $# -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    show_help
    exit 0
fi

SQL_FILE="$1"
OPTION="$2"

# Kiểm tra file tồn tại
if [ ! -f "$SQL_FILE" ]; then
    echo -e "${RED}❌ File không tồn tại: $SQL_FILE${NC}"
    exit 1
fi

echo -e "${BLUE}📄 File: $SQL_FILE${NC}"

# Xử lý theo option
case "$OPTION" in
    "--info")
        echo -e "${YELLOW}📊 Hiển thị thông tin file...${NC}"
        python3 -m src.main info "$SQL_FILE"
        ;;
    "--split-only")
        echo -e "${YELLOW}✂️  Chia nhỏ file...${NC}"
        python3 -m src.main split-file "$SQL_FILE"
        ;;
    "--no-split")
        echo -e "${YELLOW}📥 Import không chia file...${NC}"
        python3 -m src.main import-sql "$SQL_FILE" --no-split
        ;;
    *)
        echo -e "${YELLOW}📥 Import với tự động chia file...${NC}"
        python3 -m src.main import-sql "$SQL_FILE"
        ;;
esac

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Hoàn tất!${NC}"
else
    echo -e "${RED}❌ Có lỗi xảy ra!${NC}"
    exit 1
fi
