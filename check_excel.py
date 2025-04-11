import pandas as pd
from pathlib import Path

# 检查Excel文件是否存在
excel_path = Path('/Users/weigu/Documents/Exercise/qzz_autoType/input_data.xlsx')
print('Excel文件存在:', excel_path.exists())

if excel_path.exists():
    # 读取Excel文件
    df = pd.read_excel(excel_path, header=None)
    print('Excel文件列数:', df.shape[1])
    print('Excel文件行数:', df.shape[0])
    print('\n前5行数据预览:')
    print(df.head())
    
    # 打印特定列的数据
    print('\n特定列的数据:')
    columns_to_check = {
        'B列(企业名称)': 1,
        'D列(省代码)': 3,
        'F列(市代码)': 5,
        'H列(区代码)': 7,
        'I列(详细地址)': 8,
        'K列(一级行业)': 10,
        'M列(二级行业)': 12
    }
    
    for col_name, col_idx in columns_to_check.items():
        if col_idx < df.shape[1]:
            print(f'{col_name} 数据示例: {df.iloc[1:6, col_idx].tolist()}')
        else:
            print(f'{col_name} 超出Excel列范围')