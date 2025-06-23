import json
from math import fabs
from pandas.core.computation.ops import Op
import requests
import logging
from typing import Optional
from config import Config
import data_random_generator
import time

import json_generator

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
        logger.debug(f"创建企业请求数据: {data}")
        
        # 检查认证信息是否有效
        if not self._check_auth():
            logger.error("认证信息无效，请更新配置文件中的认证信息")
            return None
             
        try:
            response = requests.post(url, data=data, headers=Config.HEADERS, timeout=30)
            
            try:
                response_json = response.json()
                logger.info(f"企业创建API响应内容: {response_json}")
                
                if response.status_code != 200 or response_json.get('code') != 200:
                    error_msg = response_json.get('msg', '未知错误')
                    logger.error(f"API响应错误: {error_msg}")
                    
                    # # 如果是认证失败，提示更新认证信息
                    # if "认证失败" in error_msg or "无法访问" in error_msg:
                    #     logger.error("认证令牌可能已过期，请更新配置文件中的认证信息")
                    return None
            except ValueError as e:
                logger.error(f"企业创建API响应不是有效的JSON: {response.text}")
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
        data = json_generator.ApiJsonGenerator.create_answer_result_json(company_id)
        logger.info(f"发送诊断请求: {url}")
        logger.debug(f"企业诊断请求数据: {data}")
        
        # 检查认证信息是否有效
        if not self._check_auth():
            logger.error("认证信息无效，请更新配置文件中的认证信息")
            return None

        try:
            json_data = json.dumps(data)
            response = requests.post(url, data=json_data, headers=Config.HEADERS, timeout=30)
                        
            try:
                response_json = response.json()
                logger.debug(f"企业诊断API响应内容: {response_json}")
                
                if response.status_code != 200 or response_json.get('code') != 200:
                    error_msg = response_json.get('msg', '未知错误')
                    logger.error(f"企业诊断API响应错误: {error_msg}")
                    return None
                    
                return response_json.get('data')
            except ValueError as e:
                logger.error(f"企业诊断API响应不是有效的JSON: {response.text}")
                return None
        except requests.exceptions.Timeout:
            logger.error(f"企业诊断API请求超时: {url}", exc_info=True)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"企业诊断API请求失败: {str(e)}", exc_info=True)
            return None

    # 生成报告
    def generate_report(self, company_id: str, diagnosis_id: str) -> Optional[str]:
        # 调用 submit 接口
        endpoint = Config.REPORT_GENERATE_ENDPOINT
        url = f"{self.base_url}{endpoint}"
        data = json_generator.ApiJsonGenerator.create_report_json(company_id, diagnosis_id)
        logger.info(f"发送诊断报告生成请求: {url}")
        logger.debug(f"诊断报告请求数据: {data}")
        
        # 检查认证信息是否有效
        if not self._check_auth():
            logger.error("认证信息无效，请更新配置文件中的认证信息")
            return False
            
        try:
            # 使用data参数而不是json参数，确保请求体格式与Postman一致
            json_data = json.dumps(data)
            response = requests.post(url, data=json_data, headers=Config.HEADERS, timeout=30)
            
           #logger.info(f"诊断报告API响应状态码: {response.json().get('code')}")
            
            try:
                response_json = response.json()
                logger.info(f"诊断报告API响应内容: {response_json}")
                
                if response.status_code != 200 or response_json.get('code') != 200:
                    error_msg = response_json.get('msg', '未知错误')
                    logger.error(f"诊断报告API响应错误: {error_msg}")
                    return False
                    
                return response_json.get('data')
            except ValueError as e:
                logger.error(f"诊断报告API响应不是有效的JSON: {response.text}")
                return False
        except requests.exceptions.Timeout:
            logger.error(f"诊断报告API请求超时: {url}", exc_info=True)
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"诊断报告API请求失败: {str(e)}", exc_info=True)
            return False

    #报告生成轮询
    def poll_report_status(self, report_id: str) -> bool:
        endpoint = Config.POLLING_ENDPOINT
        url = f"{self.base_url}{endpoint}"
        headers = Config.HEADERS.copy()
        data = {
            "jobKey": report_id
        }

        logger.info(f"轮询 AI 报告生成状态: {url}")
        logger.debug(f"AI 报告请求数据: {data}")
        try:            
            # 发起POST请求获取报告状态
            json_data = json.dumps(data)
            response = requests.post(url, data=json_data, headers=headers, timeout=30)

            if not response or not response.json():
                logger.error("获取AI报告状态失败: 无效的API响应")
                return False
                
            response_data = response.json()
            # 从响应数据中获取状态值，默认为空字符串
            status = response_data.get("data", {}).get("status", "")
            
            # 轮询直到报告状态变为"1"或"-1"(1：成功，-1：失败， 0：生成中)
            while status == 0:
                logger.info(f"AI 报告状态: {status}")
                logger.info("....AI 报告生成中，正在等待....")
                time.sleep(20)  # 每20秒轮询一次
                response = requests.post(url, data=json_data, headers=headers, timeout=30)
                if not response or not response.json():
                    logger.error("获取 AI 报告状态失败: 无效的API响应")
                    return False
                    
                response_data = response.json()
                status = response_data.get("data", {}).get("status", "")

            # 最终报告状态
            if status == 1:
                logger.info("----AI 报告生成成功----")
                return True
            else:
                logger.error("----AI 报告生成失败----")
                return False
            
        except requests.exceptions.Timeout:
            logger.error(f"AI 报告轮询API请求超时: {url}", exc_info=True)
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f" AI 报告轮询API请求失败: {str(e)}", exc_info=True)
            return False
