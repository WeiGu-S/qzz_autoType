import pandas as pd
import json
from typing import Iterator, Dict
from pathlib import Path

class ExcelDataReader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.required_columns = [
            'company_name',
            'legal_representative',
            'registered_capital',
            'establishment_date'
        ]

    def validate_file(self) -> None:
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel文件不存在: {self.file_path}")
        if self.file_path.suffix not in ['.xlsx', '.xls']:
            raise ValueError("仅支持Excel文件格式(.xlsx/.xls)")

    def read_data(self) -> Iterator[Dict]:
        self.validate_file()
        df = pd.read_excel(self.file_path, engine='openpyxl')
        
        # 验证必要字段
        missing_cols = [col for col in self.required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Excel缺少必要列: {', '.join(missing_cols)}")

        for _, row in df.iterrows():
            yield {
                "company_name": str(row['company_name']),
                "legal_representative": str(row['legal_representative']),
                "registered_capital": float(row['registered_capital']),
                "establishment_date": row['establishment_date'].strftime('%Y-%m-%d'),
                "contact_info": {
                    "phone": str(row.get('contact_phone', '')),
                    "email": str(row.get('contact_email', ''))
                }
            }