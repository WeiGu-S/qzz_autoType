// 定义密钥
const CryptoJS = require("crypto-js")
const key = CryptoJS.enc.Utf8.parse("jdnyjym2023wmudrpoilcsxq"); // 32字节
  // 解密函数
function Decrypt(ciphertext) {
  if(!ciphertext){
    return null;
  }

  const decrypt = CryptoJS.AES.decrypt(ciphertext, key, {
    mode:CryptoJS.mode.ECB,
    padding: CryptoJS.pad.Pkcs7
  });
  const decryptedStr = decrypt.toString(CryptoJS.enc.Utf8)
  return decryptedStr.toString();
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

// 测试
// const plaintext = "李四";
// const encrypted = Encrypt(plaintext);
// console.log("加密结果:", encrypted);

// console.log("解密结果:", Decrypt(encrypted));

