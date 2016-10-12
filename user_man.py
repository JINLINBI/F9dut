import mysql.connector
import os
class User_man(object):
    def __init__(self):
        self.conn=mysql.connector.connect(user='jinlin',password='password',database='F9dut')
        self.passwdFileName='passwd'
        if os.path.isfile(self.passwdFileName):
            self.passwd=open(self.passwdFileName,'r')
        else :
            self.passwd=None
        self.cursor=self.conn.cursor()
    def getUser(self):
        #execute('')
        ID=input("Input ID to crack:")
        return ID
    def getPasswd(self):
        if self.passwd:
            return self.passwd.readline()[:-1]
    def reloadFile(self):
        if self.passwd:
            self.passwd.close()
        else :
            self.passwd=open(self.passwdFileName,'r')
        return True
    def setUser(self,ID,name,passwd):
        execute='select ID from user where ID=%s'%ID
        self.cursor.execute(execute)
        result=self.cursor.fetchmany()
        if len(result)==0:
            execute='insert into user(ID,name,passwd) values(%d,"%s","%s")'%(ID,name,passwd)
	    self.cursor.execute(execute)
	self.conn.commit()
if __name__=='__main__':
    user_man=User_man()
    user_man.setUser(3114002782,'zhangyiyi','fucksociety')
