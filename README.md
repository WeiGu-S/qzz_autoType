# 企业诊断自动化处理系统

## 功能概述
实现从Excel读取企业信息，通过API完成企业创建->企业诊断->报告生成的完整业务流程自动化处理

## API接口调用说明
1. 企业创建接口：POST请求，需提供企业基本信息
2. 企业诊断接口：POST请求，需提供企业ID，返回诊断ID
3. 报告生成接口：PSOT请求，需提供诊断ID 和企业ID，返回报告ID
4. AI 报告生成轮询接口：POST请求，需提供报告ID

所有API请求需在headers中添加:
```
Content-Type: application/json
Authorization: Bearer {access_token}
Cookie:{cookie}
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
  - 企业名称(enterpriseName)
  - 省市区(province, city, district)
  - 所属行业(first_industry_name, second_industry_name)
  - 地址(address)
- 建议使用Excel 2010+格式(.xlsx)
- 文件需命名为input_data.xlsx并放置在项目根目录

## 日志查看
- 日志文件保存在logs/process.log
- 按日期分割日志文件，文件名格式为process.log.YYYY-MM-DD
- 保留最近30天的日志记录

## 手机号和姓名随机生成
- 随机生成姓名和手机号
- 使用 CryptoJS 对姓名和手机号进行加密

