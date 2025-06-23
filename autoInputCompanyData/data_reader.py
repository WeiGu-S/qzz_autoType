from ast import Yield
from logging import Logger
import pandas as pd
from typing import Iterator, Dict, Union
from pathlib import Path
import random
import json

import data_random_generator
import json_generator

# 读取Excel文件中的公司信息并包装为 Json 格式
class CompanyInfoReader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        # B列(企业名称)，D列(省代码)，F列(市代码)，H列(区代码)，I列(详细地址)，K列(一级行业)，M列(二级行业)，N列(成立时间)
        self.column_mapping = {
            'enterpriseName': 1,  # B列(企业名称)
            'provinceCode': 3,    # D列(省代码)
            'cityCode': 5,        # F列(市代码)
            'districtCode': 7,    # H列(区代码)
            'location': 9,        # J列(位置)
            'address': 11,         # L列(详细地址)
            'firstIndustryId': 13, # N列(一级行业)
            'secondIndustryId': 15, # P列(二级行业)
            #'establishmentTime': 13, # N列(成立时间)
        }
        # 保留required_columns用于生成完整的JSON结构
        self.required_columns = list(self.column_mapping.keys())

    def validate_file(self) -> None:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel文件不存在: {self.file_path}")
        if self.file_path.suffix not in ['.xlsx', '.xls']:
            raise ValueError("仅支持Excel文件格式(.xlsx/.xls)")

    def _validate_geo_code(self, code: str, code_type: str) -> None:
        if not code.isdigit():
            raise ValueError(f"{code_type}必须为数字字符串")
        
        # length_map = {"province": 2, "city": 4, "district": 6}
        # if len(code) != length_map[code_type.split('Code')[0].lower()]:
        #     raise ValueError(f"{code_type}长度不符合规范，应为{length_map[code_type.split('Code')[0].lower()]}位数字")

    def read_data(self) -> Iterator[Dict]:
        self.validate_file()
        # 使用header=None读取Excel，因为我们将使用列索引而不是列名
        df = pd.read_excel(self.file_path, engine='openpyxl', header=None)
        
        # 检查Excel是否有足够的列
        max_col_index = max(self.column_mapping.values())
        if df.shape[1] <= max_col_index:
            raise ValueError(f"Excel文件列数不足，需要至少{max_col_index+1}列")

        # 跳过前2行，从第3行开始读取数据
        for idx, row in df.iterrows():
            if idx < 2:  # 跳过前2行
                continue
                
            # 检查是否为空行或所有关键字段都为空
            if pd.isna(row).all() or (
                pd.isna(row[self.column_mapping['enterpriseName']]) and 
                pd.isna(row[self.column_mapping['provinceCode']]) and
                pd.isna(row[self.column_mapping['firstIndustryId']])
            ):
                continue  # 跳过空行
                
            # 使用列索引获取数据，处理可能的空值
            enterprise_name = row[self.column_mapping['enterpriseName']] if pd.notnull(row[self.column_mapping['enterpriseName']]) else f"企业{idx}"
            province_code = int(row[self.column_mapping['provinceCode']]) if pd.notnull(row[self.column_mapping['provinceCode']]) else 110000
            city_code = int(row[self.column_mapping['cityCode']]) if pd.notnull(row[self.column_mapping['cityCode']]) else 110100
            district_code = int(row[self.column_mapping['districtCode']]) if pd.notnull(row[self.column_mapping['districtCode']]) else 110101
            location = row[self.column_mapping['location']] if pd.notnull(row[self.column_mapping['location']]) else '默认位置'
            address = row[self.column_mapping['address']] if pd.notnull(row[self.column_mapping['address']]) else '默认地址'
            first_industry_id = int(row[self.column_mapping['firstIndustryId']]) if pd.notnull(row[self.column_mapping['firstIndustryId']]) else 10057
            second_industry_id = int(row[self.column_mapping['secondIndustryId']]) if pd.notnull(row[self.column_mapping['secondIndustryId']]) else 359

            # 调用json_generator中的方法生成企业数据字典
            yield json_generator.ApiJsonGenerator.create_company_info_json(enterprise_name, province_code, city_code, district_code, location, address, first_industry_id, second_industry_id)
