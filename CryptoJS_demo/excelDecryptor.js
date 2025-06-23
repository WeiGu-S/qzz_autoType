// Excel解密工具 - 读取Excel中的指定列，使用CryptoJS解密后写回
const fs = require('fs');
const path = require('path');
const XLSX = require('xlsx');
const { Decrypt } = require('./cryptojs.js');

/**
 * 读取Excel文件中指定列的数据，解密后写回
 * @param {string} filePath - Excel文件路径
 * @param {string} inputColumn - 要解密的列（例如：'A'、'B'等）
 * @param {string} outputColumn - 解密结果写入的列（例如：'C'、'D'等）
 * @param {number} startRow - 开始处理的行号（从1开始计数，包含表头）
 * @param {boolean} hasHeader - 是否包含表头
 * @returns {boolean} - 处理是否成功
 */
function decryptExcelColumn(filePath, inputColumns, outputColumns, startRow = 2, hasHeader = true) {
  try {
    // 检查文件是否存在并且有写入权限
    try {
      if (!fs.existsSync(filePath)) {
        console.error(`文件不存在: ${filePath}`);
        return false;
      }
      // 检查文件权限
      fs.accessSync(filePath, fs.constants.R_OK | fs.constants.W_OK);
      console.log(`文件存在且具有读写权限: ${filePath}`);
    } catch (error) {
      console.error(`文件权限错误: ${error.message}`);
      return false;
    }

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

    console.log('开始解密数据...');
    let successCount = 0;
    let failureCount = 0;

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
          // 解密单元格值
          const decryptedValue = Decrypt(cell.v.toString());
          if (decryptedValue === null) {
            console.error(`解密失败：单元格 ${inputCellAddress} 的值 "${cell.v}" 无法解密`);
            continue;
          }
          // 写入解密后的值到输出列
          worksheet[outputCellAddress] = { t: 's', v: decryptedValue };
          
          // 确保工作表范围包含新添加的单元格
          const outputCol = outputColumn.replace(/[0-9]/g, '');
          const outputRow = parseInt(outputCellAddress.replace(/[^0-9]/g, ''), 10) - 1;
          const outputColIndex = XLSX.utils.decode_col(outputCol);
          
          // 更新工作表范围
          const range = XLSX.utils.decode_range(worksheet['!ref']);
          if (outputColIndex > range.e.c) {
            range.e.c = outputColIndex;
            worksheet['!ref'] = XLSX.utils.encode_range(range);
          }
          
          successCount++;
        } else {
          failureCount++;
        }
      }
    }
    
    // 检查目标目录是否可写
    const targetDir = path.dirname(filePath);
    try {
      fs.accessSync(targetDir, fs.constants.W_OK);
    } catch (error) {
      console.error(`目标目录无写入权限: ${error.message}`);
      return false;
    }

    // 检查是否有其他进程正在处理该文件
    const lockFile = `${filePath}.lock`;
    if (fs.existsSync(lockFile)) {
      console.error('文件正在被其他进程处理，请稍后再试');
      return false;
    }

    // 创建锁文件
    try {
      fs.writeFileSync(lockFile, process.pid.toString());
    } catch (error) {
      console.error('创建锁文件失败:', error);
      return false;
    }

    // 使用临时文件写入（确保使用正确的扩展名）
    const tempPath = path.join(path.dirname(filePath), `temp_${Date.now()}.xlsx`);
    try {
      // 先写入临时文件
      XLSX.writeFile(workbook, tempPath);
      
      // 验证临时文件是否写入成功
      if (!fs.existsSync(tempPath)) {
        console.error('临时文件写入失败');
        return false;
      }
      
      // 备份原文件
      const backupPath = `${filePath}.backup`;
      fs.copyFileSync(filePath, backupPath);
      
      // 用临时文件替换原文件
      fs.renameSync(tempPath, filePath);
      
      // 删除备份文件
      fs.unlinkSync(backupPath);

      // 删除锁文件
      fs.unlinkSync(lockFile);
      
      console.log('\n解密处理完成:');
      console.log(`- 成功解密: ${successCount} 个单元格`);
      console.log(`- 解密失败: ${failureCount} 个单元格`);
      console.log(`- 处理列: ${inputColumns.join(',')} -> ${outputColumns.join(',')}`);
      return true;
    } catch (error) {
      console.error('文件写入过程出错:', error);
      // 清理临时文件和锁文件
      try {
        if (fs.existsSync(tempPath)) {
          fs.unlinkSync(tempPath);
        }
        if (fs.existsSync(lockFile)) {
          fs.unlinkSync(lockFile);
        }
      } catch (cleanupError) {
        console.error('清理临时文件失败:', cleanupError);
      }
      return false;
    }
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
    console.log('用法: node excelDecryptor.js <Excel文件路径> <输入列(多列用逗号分隔)> <输出列(多列用逗号分隔)> [起始行=2] [是否有表头=true]');
    console.log('示例: node excelDecryptor.js ./data.xlsx A,B C,D 2 true');
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
  
  return decryptExcelColumn(filePath, inputColumns, outputColumns, startRow, hasHeader);
}

// 如果直接运行此脚本，则处理命令行参数
if (require.main === module) {
  processCommandLineArgs();
}

// 导出函数，以便其他模块使用
module.exports = {
  decryptExcelColumn
};