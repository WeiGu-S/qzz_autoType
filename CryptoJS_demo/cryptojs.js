// 定义密钥
const CryptoJS = require("crypto-js")
const key = CryptoJS.enc.Utf8.parse("jdnyjym2023wmudrpoilcsxq"); // 32字节
  // 解密函数
function Decrypt(ciphertext) {
  try {
    if(!ciphertext){
      return null;
    }

    const decrypt = CryptoJS.AES.decrypt(ciphertext, key, {
      mode:CryptoJS.mode.ECB,
      padding: CryptoJS.pad.Pkcs7
    });
    
    const decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
    if (!decryptedStr) {
      console.error('解密失败：无法解析结果');
      return null;
    }
    
    return decryptedStr;
  } catch (error) {
    console.error('解密过程出错:', error.message);
    return null;
  }
}
function Encrypt(data) {
  if(!data){
    return '';
  }
  const encrypted = CryptoJS.AES.encrypt(data, key, {
    mode: CryptoJS.mode.ECB,
    padding: CryptoJS.pad.Pkcs7
  }).toString();
  return encrypted
}

module.exports = {
  Encrypt,
  Decrypt
};
