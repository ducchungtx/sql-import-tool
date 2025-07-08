#!/bin/bash

# Màu sắc cho output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 SQL Import Tool - Quick Setup${NC}"
echo "=================================="

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 không được tìm thấy. Vui lòng cài đặt Python3.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python3 đã được cài đặt${NC}"

# Cài đặt dependencies
echo -e "${YELLOW}📦 Đang cài đặt dependencies...${NC}"
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies đã được cài đặt thành công${NC}"
else
    echo -e "${RED}❌ Lỗi cài đặt dependencies${NC}"
    exit 1
fi

# Test config
echo -e "${YELLOW}🔧 Kiểm tra config database...${NC}"
if [ -f "config/database.yaml" ]; then
    echo -e "${GREEN}✓ File config database.yaml tồn tại${NC}"

    # Hiển thị config hiện tại
    echo -e "${BLUE}📋 Config hiện tại:${NC}"
    cat config/database.yaml
    echo

    # Test kết nối
    echo -e "${YELLOW}🔌 Test kết nối database...${NC}"
    python -m src.main test-connection

else
    echo -e "${RED}❌ Không tìm thấy file config/database.yaml${NC}"
    echo -e "${YELLOW}💡 Vui lòng tạo file config/database.yaml với nội dung:${NC}"
    echo "host: your_host"
    echo "user: your_user"
    echo "password: your_password"
    echo "database: your_database"
    echo "port: 3306"
fi

echo
echo -e "${GREEN}🎉 Setup hoàn tất!${NC}"
echo -e "${BLUE}💡 Để xem hướng dẫn sử dụng:${NC} python -m src.main help"
