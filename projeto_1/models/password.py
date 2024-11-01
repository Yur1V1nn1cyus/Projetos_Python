from datetime import datetime
from pathlib import Path
class BaseModel:
 
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / 'db'
    
    def save (self):
        table_path = Path(self.DB_DIR / f'{self.__class__.__name__}.txt')
        if not table_path.exists():
            table_path.touch()
        with open(table_path, 'a') as arq:
            arq.write(" | ".join(list(map(str, self.__dict__.values()))))
            arq.write('\n')

    @classmethod
    def get (cls ):
        table_path = Path(cls.DB_DIR / f'{cls.__name__}.txt')
        if not table_path.exists():
            table_path.touch()
        with open(table_path, 'r') as arq:
            x = arq.readlines ()
        
        result = [] #para usar os atributos no arrai
        
        atrib = vars(cls())

        for i in x : 
            split_v = i.split('|')
            tmp_dict = dict(zip(atrib, split_v))
            result.append(tmp_dict)
        return result

class passdate (BaseModel):
    def __init__(self, domain = None, password = None, expire = False):
        self.domain = domain
        self.password = password
        self.create_at = datetime.now().isoformat()