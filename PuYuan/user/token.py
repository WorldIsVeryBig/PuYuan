from itsdangerous import URLSafeTimedSerializer as utsr
from PuYuan.settings import SECRET_KEY
from base64 import b64encode ,b64decode
import base64, re, json

class email_token():
    def __init__(self, sk=SECRET_KEY):
        self.sk = sk
        a = bytes(sk, 'utf-8')
        self.salt = base64.encodestring(a).decode().replace('\n','')
    def generate_validate_token(self, username):
        serializer = utsr(self.sk)
        return serializer.dumps(username, self.salt)
    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.sk)
        return serializer.loads(token,
        salt=self.salt,
        max_age=expiration)