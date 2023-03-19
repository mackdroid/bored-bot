# simple json, key based database system, nothing fancy really
from os import path
import json
from tkinter.messagebox import NO

class DB():
    def __init__(self):
        if path.exists("db.json"):
            self.db_file = open("db.json")
        else:
            self.db_file = open("db.json","x")
            json.dump({},self.db_file)
        self.db = json.loads(self.db_file.read())
        
    def write(self):
        json.dump(self.db,open("db.json","w"))
        
    def root_handle(self,root):
        if root == None:
            db = self.db
        else:
            root = root.split("/")
            db = self.db
            for i in root:
                if i in db.keys():
                    db = db[i]
                else:
                    raise IndexError
        return db
        
    def upd_val(self,key,val,root=None):
        db = self.root_handle(root)
        if type(val) == dict:
            raise TypeError
        else:
            db[key]=val
            self.write()
    
    def del_val(self,key,root=None):
        db = self.root_handle(root)
        if key in db.keys():
            db[key]=None
            self.write()
        else:
            raise KeyError
        
    def del_key(self,key,root=None):
        db = self.root_handle(root)
        del db[key]
        self.write()

    