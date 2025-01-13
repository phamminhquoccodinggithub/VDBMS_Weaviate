import pandas as pd

# Đường dẫn tới file Excel
file_path = 'data/description.xls'  # Thay bằng đường dẫn tới file Excel của bạn

# Đọc dữ liệu từ file Excel
data = pd.read_excel(file_path)
print(data['Mô tả'])
# Tạo cột mới bằng cách ghép nội dung của cột "Mô tả" và "Kết luận"
data['Mô tả + Kết luận'] = (
    data['Mô tả'].fillna('').astype(str) + " " +
    data['Kết luận'].fillna('').astype(str)
)

# Lựa chọn các cột cần giữ lại
columns_to_keep = ['STT', 'Mã BN', 'Họ tên BN', 'Phái', 'Ngày sinh', 'Tuổi',
                   'Địa chỉ', 'Mã ICD', 'Chẩn đoán', 'Mô tả + Kết luận']
data_reduced = data[columns_to_keep]

# Chuyển đổi DataFrame thành định dạng JSON
json_output = data_reduced.to_json(
    orient='records', force_ascii=False, indent=4)

# Lưu file JSON
output_file_path = 'data/description.json'  # Đường dẫn lưu file JSON
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write(json_output)

print(f"File JSON đã được lưu tại: {output_file_path}")
