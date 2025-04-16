// 创建示例Excel文件用于测试加密功能
const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

/**
 * 创建一个示例Excel文件，包含姓名和电话号码数据
 * @param {string} outputPath - 输出文件路径
 */
function createSampleExcel(outputPath = './sample_data.xlsx') {
  // 示例数据
  const names = [
    "赵文辉", "钱敏静", "孙昊磊", "李俊杰", "周雪玲",
    "吴志超", "郑雨彤", "王瑞阳", "冯雅欣", "陈逸飞"
  ];
  
  const phones = [
    "15030933419", "18564642039", "13324035785", "13760587615", "18036715229",
    "18530916494", "13366355290", "15231854351", "17133923408", "18996223808"
  ];
  
  // 创建工作簿和工作表
  const workbook = XLSX.utils.book_new();
  
  // 准备数据
  const data = [];
  
  // 添加表头
  data.push(["姓名", "电话", "加密后姓名", "加密后电话"]);
  
  // 添加数据行
  for (let i = 0; i < names.length; i++) {
    data.push([names[i], phones[i], "", ""]);
  }
  
  // 将数据转换为工作表
  const worksheet = XLSX.utils.aoa_to_sheet(data);
  
  // 将工作表添加到工作簿
  XLSX.utils.book_append_sheet(workbook, worksheet, "数据");
  
  // 写入文件
  XLSX.writeFile(workbook, outputPath);
  
  console.log(`示例Excel文件已创建: ${outputPath}`);
  console.log('现在可以使用以下命令加密数据:');
  console.log(`node excelEncryptor.js ${outputPath} A C`); // 加密姓名
  console.log(`node excelEncryptor.js ${outputPath} B D`); // 加密电话
}

// 如果直接运行此脚本，则创建示例文件
if (require.main === module) {
  createSampleExcel();
}

module.exports = { createSampleExcel };