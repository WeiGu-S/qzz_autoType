// Excel加密工具 - 读取Excel中的指定列，使用CryptoJS加密后写回
const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');
const { Encrypt } = require('./cryptojs.js');
/**
 * 读取Excel文件中指定列的数据，加密后写回
 * @param {string} filePath - Excel文件路径
 * @param {string} inputColumn - 要加密的列（例如：'A'、'B'等）
 * @param {string} outputColumn - 加密结果写入的列（例如：'C'、'D'等）
 * @param {number} startRow - 开始处理的行号（从1开始计数，包含表头）
 * @param {boolean} hasHeader - 是否包含表头
 * @returns {boolean} - 处理是否成功
 */
function encryptExcelColumn(filePath, inputColumns, outputColumns, startRow = 2, hasHeader = true) {
  try {
    // 检查文件是否存在
    if (!fs.existsSync(filePath)) {
      console.error(`文件不存在: ${filePath}`);
      return false;
    }
    console.log(`文件存在: ${filePath}`);

    // 读取Excel文件
    const workbook = XLSX.readFile(filePath);
    const sheetName = workbook.SheetNames[0]; // 默认使用第一个工作表
    const worksheet = workbook.Sheets[sheetName];
    
    // 获取工作表范围
    const range = worksheet['!ref'] ? XLSX.utils.decode_range(worksheet['!ref']) : {s:{c:0,r:0},e:{c:0,r:0}};    
    // 调整起始行（Excel是从1开始，但XLSX库是从0开始）
    const actualStartRow = Math.max(startRow - 1, 0); // 确保不小于0
    
    // 检查是否有有效的数据范围
    if (!worksheet['!ref']) {
      console.log('工作表为空');
      return false;
    }
    
    // 确保range.e.r是有效的数字
    if (typeof range.e.r !== 'number' || isNaN(range.e.r)) {
        console.log(range.e.r);
        console.log('工作表范围无效');
        return false;
    }
    
    if (range.e.r < 0) {
      console.log('工作表没有数据行');
      return false;
    }
    
    if (actualStartRow > range.e.r) {
      console.log(`起始行${actualStartRow+1}大于数据最后行${range.e.r+1}`);
      return false;
    }
    console.log(`有效数据行范围: 第${actualStartRow+1}行到第${range.e.r+1}行`);

    // 遍历指定列的每一行
    for (let row = actualStartRow; row <= range.e.r; row++) {
      // 遍历每对输入输出列
      for (let i = 0; i < inputColumns.length; i++) {
        const inputColumn = inputColumns[i];
        const outputColumn = outputColumns[i];
        
        // 获取输入单元格地址
        const inputCellAddress = `${inputColumn}${row + 1}`;
        // 获取输出单元格地址
        const outputCellAddress = `${outputColumn}${row + 1}`;
        
        // 获取单元格值
        const cell = worksheet[inputCellAddress];
        if (cell && cell.v) {
          // 加密单元格值
          const encryptedValue = Encrypt(cell.v.toString())
          // 写入加密后的值到输出列
          worksheet[outputCellAddress] = { t: 's', v: encryptedValue };
        }
      }
    }
    
    // 写回Excel文件
    XLSX.writeFile(workbook, filePath);
    //console.log(`成功处理文件: ${filePath}`);
    console.log(`已将 ${inputColumns.join(',')} 列数据加密并分别写入 ${outputColumns.join(',')} 列`);
    return true;
  } catch (error) {
    console.error('处理Excel文件时出错:', error);
    return false;
  }
}

/**
 * 命令行参数处理
 */
function processCommandLineArgs() {
  const args = process.argv.slice(2);
  
  if (args.length < 3) {
    console.log('用法: node excelEncryptor.js <Excel文件路径> <输入列(多列用逗号分隔)> <输出列(多列用逗号分隔)> [起始行=2] [是否有表头=true]');
    console.log('示例: node excelEncryptor.js ./data.xlsx A,B C,D 2 true');
    process.exit(1);
  }
  
  const filePath = args[0];
  const inputColumns = args[1].split(',').map(col => col.trim().toUpperCase());
  const outputColumns = args[2].split(',').map(col => col.trim().toUpperCase());
  if (inputColumns.length !== outputColumns.length) {
    console.error('输入列和输出列数量不匹配');
    process.exit(1);
  }
  const startRow = args[3] ? parseInt(args[3]) : 2;
  const hasHeader = args[4] ? args[4].toLowerCase() === 'true' : true;
  
  return encryptExcelColumn(filePath, inputColumns, outputColumns, startRow, hasHeader);
}

// 如果直接运行此脚本，则处理命令行参数
if (require.main === module) {
  processCommandLineArgs();
}

// 导出函数，以便其他模块使用
module.exports = {
  encryptExcelColumn
};