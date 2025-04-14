import json
import logging
import time
import random
from data_reader import CompanyInfoReader
from api_client import APIClient
from logger import setup_logger

# 企业录入处理流程
def process_company(api: APIClient, company_data: json) -> bool:
    logger = logging.getLogger(__name__)
    
    try:
        # 验证输入数据是否为有效的JSON字符串
        try:
            company_info = json.loads(company_data)
        except json.JSONDecodeError as je:
            logger.info(f"无效的JSON数据格式: {str(je)}")
            return False
            
        logger.info(f"开始处理企业: {company_info['enterpriseName']}")       
        # 创建企业
        company_id = api.create_company(company_data)
        if not company_id:
            logger.error("企业创建失败")
            return False
            
        # # 启动诊断
        # report_id = api.start_diagnosis(company_id)
        # if not report_id:
        #     logger.error(f"企业诊断失败: {company_id}")
        #     return False
        
        # # 生成报告
        # if not api.generate_report(company_id, report_id):
        #     logger.error(f"报告生成失败: {report_id}")
        #     return False
            
        # logger.info(f"流程完成: 企业ID={company_id} 报告ID={report_id}")
        return True
        
    except json.JSONDecodeError as je:
        logger.error(f"JSON解析错误: {str(je)}", exc_info=True)
        return False
    except KeyError as ke:
        logger.error(f"缺少必要的字段: {str(ke)}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"处理流程异常: {str(e)}", exc_info=True)
        return False

def main():
    setup_logger()
    logger = logging.getLogger(__name__)
    
    try:
        api = APIClient()
        reader = CompanyInfoReader("input_data.xlsx")
        
        # 先将所有数据读取到列表中
        company_data_list = []
        for data in reader.read_data():
            company_data_list.append(data)
        
        total_records = len(company_data_list)
        
        success_count = 0
        failure_count = 0
        
        for idx, company_data in enumerate(company_data_list, 1):
            logger.info(f"正在处理第{idx}条记录，共{total_records}条")
            company_data = json.dumps(company_data)  # 将字典转换为JSON字符串
            if process_company(api, company_data):
                success_count += 1
            else:
                failure_count += 1
                # 如果第一条记录就失败，可能是认证问题，提供更详细的提示
                if idx == 1 and failure_count == 1:
                    logger.error("认证失败，请检查配置文件")
                    break
            
            # # 如果不是最后一条记录，添加随机延时3-5分钟
            # if idx < total_records:
            #     sleep_time = random.randint(180, 300)  # 3-5分钟的随机秒数
            #     logger.info(f"等待{sleep_time}秒后处理下一条记录...")
            #     time.sleep(sleep_time)
        
    except Exception as e:
        logger.error(f"主程序异常: {str(e)}", exc_info=True)
    
    logger.info(f"处理完成 成功: {success_count} 失败: {failure_count}")

if __name__ == "__main__":
    main()