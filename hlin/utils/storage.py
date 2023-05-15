from tinydb import TinyDB , Query
from hlin.config import Settings , DAILY_QUOTES_CFG_TABLE

settings = Settings()

class UserConfig:
    """Wraps TinyDB utilities to write , update and read user's configs"""
    def __init__(self ,filepath , table = DAILY_QUOTES_CFG_TABLE):
        self.db = TinyDB(filepath)
        self.table = self.db.table(table)
        self.User = Query()
    def write_config(self, id : int, fragment : dict):
        doc = {'discord_id':id} | fragment
        if len(self.table.search(self.User.discord_id == id)) >= 1 :
            self.table.update(doc)
        else :
            self.table.insert(doc)
    def read_config(self, id ):
        if id in ['all','*']:
            config = self.table.all()
            return config
        else :
            config = self.table.search(self.User.discord_id == id)
            return config