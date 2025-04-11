# 企业诊断自动化处理系统

## 功能概述
实现从Excel读取企业信息，通过API完成企业创建->企业诊断->报告生成的完整业务流程自动化处理

## API接口调用说明
1. 企业创建接口：POST请求，需提供企业基本信息
2. 企业诊断接口：POST请求，需提供企业ID
3. 报告生成接口：PSOT请求，需提供报告ID 和企业 ID

所有API请求需在headers中添加:
```
Content-Type: application/json
Authorization: Bearer {access_token}
```

## 环境要求
- Python 3.8+
- 依赖包详见requirements.txt

## 快速开始
```bash
# 安装依赖
pip install -r requirements.txt

# 准备Excel数据文件
cp your_data.xlsx input_data.xlsx

# 运行主程序
python main.py
```

## 数据文件格式要求
- 必须包含字段：
  - 企业名称(company_name)
  - 注册资本(registered_capital)
  - 成立日期(establish_date)
- 字段格式要求：
  - 注册资本需为数字格式
  - 成立日期需为YYYY-MM-DD格式
- 建议使用Excel 2010+格式(.xlsx)
- 文件需命名为input_data.xlsx并放置在项目根目录

## 日志查看
- 日志文件保存在logs/process.log
- 保留最近3个日志备份，单个日志最大50MB