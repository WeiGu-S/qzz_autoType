# Excel数据加密工具

这个工具可以自动读取Excel文件中的指定列数据，使用AES加密算法进行加密，然后将加密结果写回到Excel文件的另一列中。

## 功能特点

- 支持读取Excel文件中的指定列数据
- 使用AES-ECB-PKCS7加密算法进行加密
- 将加密结果写回到Excel文件的指定列
- 支持命令行参数配置

## 使用方法

### 命令行使用

```bash
node excelEncryptor.js <Excel文件路径> <输入列> <输出列> [起始行=2] [是否有表头=true]
```

参数说明：
- `<Excel文件路径>`: 要处理的Excel文件路径
- `<输入列>`: 要加密的数据所在列（例如：A、B等）
- `<输出列>`: 加密结果写入的列（例如：C、D等）
- `[起始行]`: 开始处理的行号，默认为2（假设第1行为表头）
- `[是否有表头]`: 是否包含表头，默认为true

### 示例

```bash
# 将data.xlsx文件中A列的数据加密后写入B列，从第2行开始处理
node excelEncryptor.js ./data.xlsx A B

# 将users.xlsx文件中C列的数据加密后写入D列，从第3行开始处理，无表头
node excelEncryptor.js ./users.xlsx C D 3 false
```

### 在其他代码中使用

```javascript
const { encryptExcelColumn } = require('./excelEncryptor');

// 将data.xlsx文件中A列的数据加密后写入B列，从第2行开始处理
encryptExcelColumn('./data.xlsx', 'A', 'B', 2, true);
```

## 准备工作

使用前请确保已安装所需依赖：

```bash
npm install xlsx crypto-js
```

## 注意事项

- 加密使用的密钥已经在代码中设置，如需更改请修改源代码中的key值
- 处理大文件时可能需要较长时间，请耐心等待
- 建议先备份Excel文件，再进行加密操作