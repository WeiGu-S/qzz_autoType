from asyncio import sleep
import json
import os
import logging
import time
import random
from data_reader import CompanyInfoReader
from api_client import APIClient
from logger import setup_logger

# 持久化文件路径(记录当前已处理数据，避免重复录入）
PROCESSED_INDICES_FILE = "processed_indices.json"

def load_processed_indices():
    """加载已处理的索引"""
    if os.path.exists(PROCESSED_INDICES_FILE):
        try:
            with open(PROCESSED_INDICES_FILE, "r") as f:
                return set(json.load(f))
        except (json.JSONDecodeError, IOError) as e:
            logging.warning(f"加载已处理索引文件失败，将新建文件: {str(e)}")
    return set()

def save_processed_indices(processed_indices):
    """保存已处理的索引"""
    try:
        with open(PROCESSED_INDICES_FILE, "w") as f:
            json.dump(list(processed_indices), f)
    except IOError as e:
        logging.error(f"保存已处理索引失败: {str(e)}")

def clear_processed_indices():
    """清空已处理的索引文件"""
    try:
        if os.path.exists(PROCESSED_INDICES_FILE):
            os.remove(PROCESSED_INDICES_FILE)
            logging.info("已清空处理记录文件")
    except IOError as e:
        logging.error(f"清空处理记录文件失败: {str(e)}")

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
    logger.info(f"company_data: {company_data}")
    if not company_id:
        logger.error("*****企业创建失败*****")
        return False
        
    # 启动诊断,获取诊断ID
    diagnosis_id = api.start_diagnosis(company_id)
    if not diagnosis_id:
        logger.error(f"*****企业诊断失败:  {company_info['enterpriseName']}，诊断 ID:{diagnosis_id}*****")
        return False
    
    # 生成报告，获取报告ID
    report_id = api.generate_report(company_id, diagnosis_id)
    if not report_id:
        logger.error(f"*****{company_info['enterpriseName']}诊断报告生成失败，报告ID: {report_id}*****")
    else:
        logger.info(f"*****{company_info['enterpriseName']}诊断报告生成成功，报告ID: {report_id}*****")

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

        total_records = len(company_data_list)
        success_count = 0
        failure_count = 0
        failure_record = []

        # 加载已处理的索引
        processed_indices = load_processed_indices()
        logger.info(f"已加载 {len(processed_indices)} 条已处理记录")

        while True:
            # 获取未处理的索引列表
            available_indices = [i for i in range(total_records) if i not in processed_indices]

            if not available_indices:
                logger.info("所有记录已处理完成")
                # 清空处理记录文件
                clear_processed_indices()
                break

            # 随机选择一个未处理的索引
            random_idx = random.choice(available_indices)
            processed_indices.add(random_idx)

            # 立即保存已处理索引，防止程序中断导致重复处理
            save_processed_indices(processed_indices)

            # 获取对应的数据
            company_data = company_data_list[random_idx]
            logger.info(f"正在处理第{random_idx + 1}条记录，共{total_records}条")

            # 处理数据
            company_data_json = json.dumps(company_data)
            if process_company(api, company_data_json):
                success_count += 1
            else:
                failure_count += 1
                failure_record.append(random_idx + 1)

            # 检查是否是最后一条记录
            if len(available_indices) == 1:
                logger.info("这是最后一条记录，处理完成后将清空记录文件")
                # 这里不添加延时，因为已经是最后一条
            elif len(available_indices) > 1:
                sleep_time = random.randint(200, 300)  # 10-20分钟的随机秒数
                logger.info(f"等待{sleep_time // 60}分钟后处理下一条记录...")
                time.sleep(sleep_time)

    except Exception as e:
        logger.error(f"主程序异常: {str(e)}", exc_info=True)
        # 发生异常时尝试保存已处理索引
        if 'processed_indices' in locals():
            save_processed_indices(processed_indices)

    finally:
        logger.info(f"处理完成: 成功 {success_count} 条, 失败 {failure_count} 条")
        if failure_count > 0:
            logger.info(f"失败记录行号: {', '.join(map(str, failure_record))}")


if __name__ == "__main__":
    main()