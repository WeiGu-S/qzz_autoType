from asyncio import sleep
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
    
    # 验证输入数据是否为有效的JSON字符串
    try:
        company_info = json.loads(company_data)
    except json.JSONDecodeError as je:
        logger.info(f"无效的JSON数据格式: {str(je)}")
        return False
        
    logger.info(f"----------------开始处理企业: {company_info['enterpriseName']}----------------")       
    # 创建企业，获取企业ID
    company_id = api.create_company(company_data)
    if not company_id:
        logger.error("企业创建失败")
        return False
        
    # 启动诊断,获取诊断ID
    diagnosis_id = api.start_diagnosis(company_id)
    if not diagnosis_id:
        logger.error(f"企业诊断失败: {company_id}")
        return False
    
    # 生成报告，获取报告ID
    report_id = api.generate_report(company_id, diagnosis_id)
    if not report_id:
        logger.error(f"{company_info['enterpriseName']}诊断报告生成失败，报告ID: {report_id}")
    else:
        logger.info(f"{company_info['enterpriseName']}诊断报告生成成功，报告ID: {report_id}")

    # 轮询报告状态
    logger.info(f"----开始轮询 AI 报告生成状态----")
    api.poll_report_status(report_id)
        
    logger.info(f"----------------{company_info['enterpriseName']}录入成功----------------")
    return True


def main():
    setup_logger()
    logger = logging.getLogger(__name__)
    
    try:
        api = APIClient()
        reader = CompanyInfoReader("input_data.xlsx")
        
        # 将所有数据读取到列表中
        company_data_list = []
        for data in reader.read_data():
            company_data_list.append(data)

        # 总记录数
        total_records = len(company_data_list)
        
        #初始化计数器
        success_count = 0
        failure_count = 0
        #记录第几条记录失败
        failure_record = []
        
        for idx, company_data in enumerate(company_data_list, 1):
            logger.info(f"正在处理第{idx}条记录，共{total_records}条")
            company_data = json.dumps(company_data)  # 将字典转换为JSON字符串
            if process_company(api, company_data):
                success_count += 1
            else:
                failure_count += 1
                failure_record.append(idx)
            
            # # 如果不是最后一条记录，添加随机延时2-3分钟
            # if idx < total_records:
            #     sleep_time = random.randint(120, 180)  # 2-3分钟的随机秒数
            #     #sleep_time = 120
            #     logger.info(f"等待{sleep_time}秒后处理下一条记录...")
            #     time.sleep(sleep_time)
        
    except Exception as e:
        logger.error(f"主程序异常: {str(e)}", exc_info=True)
    
    logger.info(f"处理完成 成功: {success_count} 失败: {failure_count}")
    if failure_count > 0:
        logger.info(f"失败记录: 第{', '.join(str(record) for record in failure_record)}行录入失败")
if __name__ == "__main__":
    main()