from ast import Yield
from logging import Logger
import pandas as pd
from typing import Iterator, Dict, Union
from pathlib import Path
import random
import json

import utils

# 读取Excel文件中的公司信息并包装为 Json 格式
class CompanyInfoReader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        # B列(企业名称)，D列(省代码)，F列(市代码)，H列(区代码)，I列(详细地址)，K列(一级行业)，M列(二级行业)，N列(成立时间)
        self.column_mapping = {
            'enterpriseName': 1,  # B列
            'provinceCode': 3,    # D列
            'cityCode': 5,        # F列
            'districtCode': 7,    # H列
            'address': 8,         # I列
            'firstIndustryId': 10, # K列
            'secondIndustryId': 12, # M列
            #'establishmentTime': 13, # N列
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

    def read_data(self) -> Iterator[dict]:
        self.validate_file()
        # 使用header=None读取Excel，因为我们将使用列索引而不是列名
        df = pd.read_excel(self.file_path, engine='openpyxl', header=None)
        
        # 检查Excel是否有足够的列
        max_col_index = max(self.column_mapping.values())
        if df.shape[1] <= max_col_index:
            raise ValueError(f"Excel文件列数不足，需要至少{max_col_index+1}列")

        # 跳过前三行，从第四行开始读取数据
        for idx, row in df.iterrows():
            if idx < 3:  # 跳过前三行
                continue
                
            # 检查是否为空行或所有关键字段都为空
            if pd.isna(row).all() or (
                pd.isna(row[self.column_mapping['enterpriseName']]) and 
                pd.isna(row[self.column_mapping['provinceCode']]) and
                pd.isna(row[self.column_mapping['firstIndustryId']])
            ):
                continue  # 跳过空行
                
            contacts = utils.RandomDataGenerator.get_name()
            telephone = utils.RandomDataGenerator.get_contact()
            
            # 使用列索引获取数据，处理可能的空值
            enterprise_name = row[self.column_mapping['enterpriseName']] if pd.notnull(row[self.column_mapping['enterpriseName']]) else f"企业{idx}"
            province_code = int(int(row[self.column_mapping['provinceCode']])) if pd.notnull(row[self.column_mapping['provinceCode']]) else '110000'
            city_code = int(int(row[self.column_mapping['cityCode']])) if pd.notnull(row[self.column_mapping['cityCode']]) else '110100'
            district_code = int(int(row[self.column_mapping['districtCode']])) if pd.notnull(row[self.column_mapping['districtCode']]) else '110101'
            address = row[self.column_mapping['address']] if pd.notnull(row[self.column_mapping['address']]) else '默认地址'
            first_industry_id = int(int(row[self.column_mapping['firstIndustryId']])) if pd.notnull(row[self.column_mapping['firstIndustryId']]) else '10057'
            second_industry_id = int(int(row[self.column_mapping['secondIndustryId']])) if pd.notnull(row[self.column_mapping['secondIndustryId']]) else '359'

            # 生成随机数据填充其他必要字段
            company_data = {
                "enterpriseName": enterprise_name,
                "contacts": contacts,
                "telephone": telephone,
                "provinceCode": province_code,
                "cityCode": city_code,
                "districtCode": district_code,
                "location": "",
                "address": address,
                "firstIndustryId": int(first_industry_id),
                "secondIndustryId": int(second_industry_id),
                "registeredCapital": int(random.randint(100, 10000)),
                "establishmentTime": "",
                "employeesNum": int(random.randint(10, 1000)),
                "enterpriseType": int(random.choice(["1", "2", "3", "4"])),
                "enterpriseScale": int(random.choice(["1", "2", "3", "4"])),
                "mainProducts": random.choice(["电子产品", "机械设备", "化工产品", "纺织品", "食品"]),
                "businessBenefits":"[{\"2021\":{\"totalAssets\":\"\",\"income\":\"\",\"profit\":\"\"}},{\"2022\":{\"totalAssets\":\"\",\"income\":\"\",\"profit\":\"\"}},{\"2023\":{\"totalAssets\":\"\",\"income\":\"\",\"profit\":\"\"}}]",
                "systemCertification": random.choice(["数据分类分级 (工业领域)", "数据安全防护体系", "两化融合管理体系", "质量管理体系", "环境管理体系", "能源管理体系", "职业健康安全管理体系", "信息安全管理体系", "数据管理能力成熟度评估模型 (DCMM)","无"]),
                "highTechEnterprise": random.choice(["国家级", "省级","市级","无"]),
                "intelligentManufacturingDemonstrationFactory": random.choice(["国家级", "省级","市级","无"]),
                "industrialInternetBenchmarkFactory": random.choice(["省级","市级","无"]),
                "specializedInnovativeLittleGiant": random.choice(["国家级", "省级","无"]),
                "applyResearchDevelopDesignSoftware": random.choice(["CAD","CAE","DBOM","CAM","数字孪生","其他","以上均无"]),
                "designSoftwareBrandModel":"",
                "applyProductionManufacturingSoftware":random.choice(["MES","APS","PLM","PDM","其他","以上均无"]),
                "manufacturingSoftwareBrandModel":"",
                "applyQualityManagementSoftware":random.choice(["QMS","LIMS","其他","以上均无"]),
                "qualitySoftwareBrandModel":"",
                "applyOperationsManagementSoftware":random.choice(["ERP","CRM","SRM","SCM","OA","BI","其他","以上均无"]),
                "operationsSoftwareBrandModel":"",
                "applyWarehouseLogisticsSoftware":random.choice(["WMS","其他","以上均无"]),
                "logisticsSoftwareBrandModel":"",
                "applyCloudService": random.choice(["公有云","私有云","混合云","无"]),
                "cloudServiceBrandModel":"",
                "networkUseSituation": random.choice(["宽带","专线","5G","无"]),
                "networkOperator":"",
                "digitalTransformFunds": int(random.choice(["1","2","3","4","5"])),
                "planCloudServiceSituation": random.choice(["设备上云","业务系统上云","资源上云（数据）","其他","以上均无"]),
                "intentionCloudBrandModel":"",
                "planApplySoftwareType":"",
                "intentionSoftwareBrandModel":""
            }
            
            # 将字典对象转换为JSON字符串后返回
            yield json.dumps(company_data, ensure_ascii=False)
