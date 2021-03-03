#coding=utf8
import hashlib

class Encryption(object):

    def __init__(self):
        pass

    def md5_pwd(self,password):

        b = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
        pwd = hashlib.md5(b.encode(encoding='UTF-8')).hexdigest()
        return pwd

    def md5_sign(self,signData ):

        pwd = hashlib.md5(signData .encode(encoding='UTF-8')).hexdigest()
        return pwd
