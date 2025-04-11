import requests
import logging
from typing import Optional, Dict
from config import Config
import utils

logger = logging.getLogger(__name__)

# 封装API请求
class APIClient:
    def __init__(self):
        self.base_url = Config.API_BASE_URL
        
    # 创建企业
    def create_company(self, data: Dict) -> Optional[str]:
        endpoint = Config.COMPANY_CREATE_ENDPOINT
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.post(url, json=data, headers=Config.HEADERS, timeout=30)
            response.raise_for_status()
            return response.json().get('data')
        except requests.exceptions.Timeout:
            logger.error(f"API请求超时: {url}", exc_info=True)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {str(e)}", exc_info=True)
            return None

    # 启动企业诊断
    def start_diagnosis(self, company_id: str) -> Optional[str]:
        endpoint = Config.COMPANY_DIAGNOSIS_ENDPOINT
        url = f"{self.base_url}{endpoint}"
        data = utils.RandomDataGenerator.create_answer_result_json(company_id)

        try:
            response = requests.post(url, json=data, headers=Config.HEADERS, timeout=30)
            response.raise_for_status()
            return response.json().get('data')
        except requests.exceptions.Timeout:
            logger.error(f"API请求超时: {url}", exc_info=True)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {str(e)}", exc_info=True)
            return None

    # 生成报告
    def generate_report(self, company_id: str, report_id: str) -> bool:
        endpoint = Config.REPORT_GENERATE_ENDPOINT
        url = f"{self.base_url}{endpoint}"
        data = utils.RandomDataGenerator.create_report_json(company_id, report_id)

        try:
            response = requests.post(url, json=data, headers=Config.HEADERS, timeout=30)
            response.raise_for_status()
            return response.json().get('msg')
        except requests.exceptions.Timeout:
            logger.error(f"API请求超时: {url}", exc_info=True)
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {str(e)}", exc_info=True)
            return False