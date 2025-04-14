import json
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
        self.auth_valid = False
        
    # 检查认证信息是否有效
    def _check_auth(self) -> bool:
        """检查认证信息是否有效，如果无效则返回False"""
        # 简单检查Authorization头是否存在
        if not Config.HEADERS.get('Authorization'):
            logger.error("配置中缺少Authorization头信息")
            return False
        return True
        
    # 创建企业
    def create_company(self, data: json) -> Optional[str]:
        endpoint = Config.COMPANY_CREATE_ENDPOINT
        url = f"{self.base_url}{endpoint}"
        logger.info(f"发送创建企业请求: {url}")
        
        # 解析JSON字符串为Python对象
        #data_obj = json.loads(data) if isinstance(data, str) else data
        #logger.info(f"请求数据: {data_obj}")
        
        # 检查认证信息是否有效
        if not self._check_auth():
            logger.error("认证信息无效，请更新配置文件中的认证信息")
            return None
        
        # 记录完整请求头信息用于调试
        headers = Config.HEADERS.copy()
        logger.debug(f"请求头信息: {headers}")
        
        try:
            # 使用data参数而不是json参数，确保请求体格式与Postman一致
            #json_data = json.dumps(data_obj) if not isinstance(data, str) else data
            response = requests.post(
                url, 
                data=data, 
                headers=headers, 
                timeout=30
            )
            
            logger.info(f"API响应状态码: {response.status_code}")
            
            try:
                response_json = response.json()
                logger.info(f"API响应内容: {response_json}")
                
                if response.status_code != 200 or response_json.get('code') != 200:
                    error_msg = response_json.get('msg', '未知错误')
                    logger.error(f"API响应错误: {error_msg}")
                    
                    # 如果是认证失败，提示更新认证信息
                    if "认证失败" in error_msg or "无法访问" in error_msg:
                        logger.error("认证令牌可能已过期，请更新配置文件中的认证信息")
                    return None
            except ValueError as e:
                logger.error(f"API响应不是有效的JSON: {response.text}")
                return None
                
            response.raise_for_status()
            return response_json.get('data')
        except requests.exceptions.Timeout:
            logger.error(f"API请求超时: {url}", exc_info=True)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {str(e)}", exc_info=True)
            return None
        except ValueError as e:
            logger.error(f"API响应解析失败: {str(e)}", exc_info=True)
            return None

    # 启动企业诊断
    def start_diagnosis(self, company_id: str) -> Optional[str]:
        endpoint = Config.COMPANY_DIAGNOSIS_ENDPOINT
        url = f"{self.base_url}{endpoint}"
        data = utils.RandomDataGenerator.create_answer_result_json(company_id)
        logger.info(f"发送诊断请求: {url}")
        #logger.info(f"请求数据: {data}")
        
        # 检查认证信息是否有效
        if not self._check_auth():
            logger.error("认证信息无效，请更新配置文件中的认证信息")
            return None
            
        # 记录完整请求头信息用于调试
        headers = Config.HEADERS.copy()
        logger.debug(f"请求头信息: {headers}")

        try:
            # 使用data参数而不是json参数，确保请求体格式与Postman一致
            json_data = json.dumps(data)
            response = requests.post(
                url, 
                data=json_data, 
                headers=headers, 
                timeout=30
            )
            
            logger.info(f"API响应状态码: {response.status_code}")
            
            try:
                response_json = response.json()
                logger.info(f"API响应内容: {response_json}")
                
                if response.status_code != 200 or response_json.get('code') != 200:
                    error_msg = response_json.get('msg', '未知错误')
                    logger.error(f"API响应错误: {error_msg}")
                    return None
                    
                return response_json.get('data')
            except ValueError as e:
                logger.error(f"API响应不是有效的JSON: {response.text}")
                return None
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
        logger.info(f"发送报告生成请求: {url}")
        #logger.info(f"请求数据: {data}")
        
        # 检查认证信息是否有效
        if not self._check_auth():
            logger.error("认证信息无效，请更新配置文件中的认证信息")
            return False
            
        # 记录完整请求头信息用于调试
        headers = Config.HEADERS.copy()
        logger.debug(f"请求头信息: {headers}")

        try:
            # 使用data参数而不是json参数，确保请求体格式与Postman一致
            json_data = json.dumps(data)
            response = requests.post(
                url, 
                data=json_data, 
                headers=headers, 
                timeout=30
            )
            
            logger.info(f"API响应状态码: {response.status_code}")
            
            try:
                response_json = response.json()
                logger.info(f"API响应内容: {response_json}")
                
                if response.status_code != 200 or response_json.get('code') != 200:
                    error_msg = response_json.get('msg', '未知错误')
                    logger.error(f"API响应错误: {error_msg}")
                    return False
                    
                return True
            except ValueError as e:
                logger.error(f"API响应不是有效的JSON: {response.text}")
                return False
        except requests.exceptions.Timeout:
            logger.error(f"API请求超时: {url}", exc_info=True)
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {str(e)}", exc_info=True)
            return False