# 企业诊断自动化处理系统

## 功能概述
实现从Excel读取企业信息，通过API完成企业创建->企业诊断->报告生成的完整业务流程自动化处理

## 环境要求
- Python 3.8+
- 依赖包详见requirements.txt

## 快速开始
```bash
# 安装依赖
pip install -r requirements.txt

# 准备Excel数据文件
cp your_data.xlsx input_data.xlsx

# 配置环境变量
cp .env.example .env

# 运行主程序
python main.py
```

## 配置文件说明
`.env`文件需配置以下参数：
```
API_BASE_URL=替换为实际API地址
COMPANY_CREATE_ENDPOINT=/v1/companies
COMPANY_DIAGNOSIS_ENDPOINT=/v1/companies/{company_id}/diagnose
REPORT_GENERATE_ENDPOINT=/v1/reports/{report_id}
```

## 数据文件格式要求
- 必须包含字段：企业名称、法定代表人、注册资本、成立日期
- 建议使用Excel 2010+格式(.xlsx)
- 文件需命名为input_data.xlsx并放置在项目根目录

## 日志查看
- 日志文件保存在logs/process.log
- 保留最近3个日志备份，单个日志最大50MB