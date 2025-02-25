import pandas as pd
import os

# path to file Excel
file_path = os.path.join('..', 'data', 'DS.xlsx')

# Read data
data = pd.read_excel(file_path)
# print(data['Mô tả'])

columns_to_keep = ['ID', 'Mô tả', 'Kết luận']
data_reduced = data[columns_to_keep]

# Convert DataFrame to JSON
json_output = data_reduced.to_json(
    orient='records', force_ascii=False, indent=4)

# Save file JSON
output_file_path = os.path.join('..', 'data', 'description2.json')
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write(json_output)

print(f"File JSON has saved at: {output_file_path}")
