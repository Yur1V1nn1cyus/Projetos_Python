import string, secrets
import hashlib, base64
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

#classe é um conj de metodos e propriedades
#self = instancia #cls = classe
#instancia e necessario quando há exemplo usuarios
#classes especificas para cada um e necessario usar atrib e met como instancia

class FernetHasher:
    RANDOM_SITRNG_CHARS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR/'pass'

    def __init__(self, key):
        if not isinstance(key, bytes):
            key = key.encode()

        self.fernet = Fernet(key)


    @classmethod
    #criar o hash aleatorio de 12 caracteres
    def random_pass(cls, length = 25):
        
        string=''
        for i in  range (length):
            string = string + secrets.choice(cls.RANDOM_SITRNG_CHARS) 
        return string 

    @classmethod
    #gerar o hash de um texto
    def create_key (cls, arquive = False):
        value = cls.random_pass()
        #desconverter para leitura em base64
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        #converter para base64
        key = base64.b64encode(hasher)
        if arquive :
            return key, cls.arquive_key(key)
        return key, None

    @classmethod
    #armazenando a key em um arquivo
    def arquive_key (cls,key):
        file = 'key.key'
        while (Path(cls.KEY_DIR / file).exists()):
            file = f'key_{cls.random_pass(length = 5)}.key'
        with open(cls.KEY_DIR/ file,'wb') as arq:
            arq.write(key)
        return cls.KEY_DIR / file

    def encriptar (self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        return self.fernet.encrypt(value)
    
    def decriptar (self, value):
        if not isinstance(value, bytes):
            value = value.encode()

        try:
            return self.fernet.decrypt(value).decode()
        except InvalidToken as e :
            return 'Token nao valido damnnn'
    