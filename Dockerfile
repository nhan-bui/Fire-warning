# Sử dụng một hình ảnh cơ sở Python với phiên bản 3.11
FROM python:3.11
# Đặt thư mục làm môi trường làm việc
WORKDIR /FireWarning
# Sao chép các tệp tin requirements.txt vào thư mục làm việc
COPY requirements.txt .

# Cài đặt các thư viện Python từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của dự án vào thư mục làm việc
COPY . .

# Chạy ứng dụng Python khi container được khởi chạy
CMD ["python", "main.py"]