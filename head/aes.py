from Crypto.Cipher import AES
from head.config import *
from Crypto.Util.Padding import pad,unpad


# AES加密函数
def aes_encode(text: str):
    password = pad(bytes(AES_KEY.encode()), 16)
    text = pad(bytes(text.encode()), 16)
    aes = AES.new(password, AES.MODE_ECB)
    en_text = aes.encrypt(text)
    return en_text.hex()


# 解密
def aes_decode(text: hex):
    text = bytes.fromhex(text)
    password = pad(bytes(AES_KEY.encode()), 16)
    aes = AES.new(password, AES.MODE_ECB)
    den_text = aes.decrypt(text)
    return unpad(den_text,16).decode("utf-8")
