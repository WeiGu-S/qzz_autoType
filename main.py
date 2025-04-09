import logging
from data_reader import ExcelDataReader
from api_client import APIClient
from logger import setup_logger

def process_company(api: APIClient, company_data: dict) -> bool:
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"开始处理企业: {company_data['company_name']}")
        
        # 创建企业
        company_id = api.create_company(company_data)
        if not company_id:
            logger.error("企业创建失败")
            return False
            
        # 启动诊断
        report_id = api.start_diagnosis(company_id)
        if not report_id:
            logger.error(f"企业诊断失败: {company_id}")
            return False
        
        # 生成报告
        if not api.generate_report(company_id, report_id):
            logger.error(f"报告生成失败: {report_id}")
            return False
            
        logger.info(f"流程完成: 企业ID={company_id} 报告ID={report_id}")
        return True
        
    except Exception as e:
        logger.error(f"处理流程异常: {str(e)}", exc_info=True)
        return False

def main():
    setup_logger()
    logger = logging.getLogger(__name__)
    
    try:
        api = APIClient()
        reader = ExcelDataReader("input_data.xlsx")
        
        success_count = 0
        failure_count = 0
        
        for idx, company_data in enumerate(reader.read_data(), 1):
            logger.info(f"正在处理第{idx}条记录")
            if process_company(api, company_data):
                success_count += 1
            else:
                failure_count += 1
            
        logger.info(f"处理完成 成功: {success_count} 失败: {failure_count}")
        
    except Exception as e:
        logger.error(f"主程序异常: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()