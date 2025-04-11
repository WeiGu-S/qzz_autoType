import pandas as pd
from typing import Iterator, Dict
from pathlib import Path
import random

import utils

class ExcelDataReader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.required_columns = [
            "enterpriseName",
            "provinceCode",
            "cityCode",
            "districtCode",
            "location",
            "address",
            "firstIndustryId",
            "secondIndustryId",
            "registeredCapital",
            "establishmentTime",
            "employeesNum",
            "enterpriseType",
            "enterpriseScale",
            "mainProducts",
        ]

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
        df = pd.read_excel(self.file_path, engine='openpyxl')
        
        # 验证必要字段
        missing_cols = [col for col in self.required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Excel缺少必要列: {', '.join(missing_cols)}")

        for _, row in df.iterrows():
            contacts = utils.randomData.nameRandomGet()
            phone = utils.randomData.contactRandomGet()

            yield {
                "enterpriseName": row['enterpriseName'],
                "contacts": contacts,
                "telephone": phone,
                "provinceCode": str(row['provinceCode']),
                "cityCode": str(row['cityCode']),
                "districtCode": str(row['districtCode']),
                "location": row['location'],
                "address": row['address'],
                "firstIndustryId": row['firstIndustryId'],
                "secondIndustryId": row['secondIndustryId'],
                "registeredCapital": str(row.get('registeredCapital', '0')),
                "establishmentTime": pd.to_datetime(row['establishmentTime']).strftime('%Y-%m') if pd.notnull(row['establishmentTime']) else '',
                "employeesNum": row['employeesNum'],
                "enterpriseType": row['enterpriseType'],
                "enterpriseScale": row['enterpriseScale'],
                "mainProducts": row['mainProducts'],
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
                "digitalTransformFunds": random.choice(["1","2","3","4","5"]),
                "planCloudServiceSituation": random.choice(["设备上云","业务系统上云","资源上云（数据）","其他","以上均无"]),
                "intentionCloudBrandModel":"",
                "planApplySoftwareType":"",
                "intentionSoftwareBrandModel":""
            }