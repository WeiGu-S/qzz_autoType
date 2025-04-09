import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_BASE_URL = os.getenv('API_BASE_URL')
    COMPANY_CREATE_ENDPOINT = os.getenv('COMPANY_CREATE_ENDPOINT')
    COMPANY_DIAGNOSIS_ENDPOINT = os.getenv('COMPANY_DIAGNOSIS_ENDPOINT')
    REPORT_GENERATE_ENDPOINT = os.getenv('REPORT_GENERATE_ENDPOINT')
    
    @classmethod
    def validate(cls):
        missing = [var for var in ['API_BASE_URL'] if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")