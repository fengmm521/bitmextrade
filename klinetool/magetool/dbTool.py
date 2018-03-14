#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-22 09:44:42

import dbm

dbpth = './db/keysdb'

class DBMObj(object):
    """docstring for ClassName"""
    def __init__(self, pth):
        self.dbpth = pth

    def inset(self,key,value):
        db = dbm.open(self.dbpth, 'c')
        db[key] = value
        db.close()

    def insetList(self,keys,values):
        if len(keys) == len(values):
            db = dbm.open(self.dbpth, 'c')
            for i in range(len(keys)):
                db[keys[i]] = values[i]
            db.close()
            return True
        else:
            return False

    def delet(self,key):
        db = dbm.open(self.dbpth, 'c')
        if key in db:
            del db[key]
        db.close()

    def update(self,key,value):
        db = dbm.open(self.dbpth, 'c')
        db[key] = value
        db.close()

    def select(self,key):
        db = dbm.open(self.dbpth, 'c')
        if key in db:
            return db[key]
        else:
            return None
        db.close()

    def allKeys(self):
        db = dbm.open(self.dbpth, 'c')
        return db.keys() 
        db.close()

def main():
    tobj = DBMObj(dbpth)
    print(tobj.allKeys())
    tobj.inset('mykey2', '111')
    print(tobj.select('mykey'))
    tobj.delet('mykey')
    print(tobj.select('mykey'))
    print(tobj.select('mykey2'))
    tobj.update('mykey2', 'dddx')
    print(tobj.select('mykey2'))
    # delet('mykey2')
    print(tobj.allKeys())

if __name__=="__main__":  
    main()

