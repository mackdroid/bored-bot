# simple json, key based database system, nothing fancy really
import json

class DB():
    def __init__(self):
        db = json.load(open("db.json").read)
        
    def write(self):
        json.dump(self.db,open("db.json"))
        
    def upd_val(self,key,val):
        if type(val) == dict:
            raise TypeError
        else:
            self.db[key]=val
            self.write()

    def del_val(self,key):
        if key in self.db.keys():
            self.db[key]=None
            self.write()
        else:
            raise KeyError
        
    def del_key(self,key):
        del self.db[key]
        self.write()

    def create_subdb(self,sdb_name):
        self.db[sdb_name]={}
        self.write()
    