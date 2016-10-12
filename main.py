#coding:utf8
#!/usr/bin/python
import code_pro
import web_pro
import parser
import user_man
import getpass
class Main(object):
    def __init__(self):
        self.user_man=user_man.User_man()
        self.code_pro=code_pro.Code_pro()
        self.web_pro=web_pro.Web_pro()
        self.parser=parser.Parser()

if __name__=='__main__':
    root_url="http://jwgldx.gdut.edu.cn"
    login_url="http://jwgldx.gdut.edu.cn/default2.aspx"
    code_url="http://jwgldx.gdut.edu.cn/CheckCode.aspx"
    print "Loading..........."
    main=Main()
    main.web_pro.viewPage(root_url)
    ID=main.user_man.getUser()
    firstTime=True
    Error=False
    while True:
        if firstTime==True and Error==False:
            passwd=main.user_man.getPasswd()
            if len(passwd)==0:
                ID=main.user_man.getUser()
                main.user_man.reloadFile()
            firstTime==False
        codePath=main.web_pro.getCode(code_url)
        code=main.code_pro.crackCode(codePath)
        loginInfo=main.web_pro.login(login_url,ID,passwd,code)
        if loginInfo ==302 :
            Error=False
            page=main.web_pro.getStudent(ID)
            name=main.parser.parserName(page)
            main.user_man.setUser(ID,name,passwd)
            print "[+]%s:login successfully!"%name
            isGo=raw_input("Continue?[Y/n]:").lower()
            if isGo=='':
                isGo='y'
            if isGo=='y' or isGo=='yes':
                ID=main.user_man.getUser()
                main.user_man.reloadFile()
            else :
                break
        elif len(loginInfo)>5:
            Error=True
            error_info=main.parser.parserError(loginInfo)
            if error_info==444:
                #main.code_pro.errorCode(codePath)
                print "[-]login failed! :CheckCode is not correct!"[:-1]
            elif error_info==555:
                main.code_pro.rightCode(codePath)
                print "[-]login failed! :Check your ID and Password!"[:-1]
            elif error_info==666:
                main.code_pro.rightCode(codePath)
                Error=False
                print "[-]password is not correct!"
            else :
                print "[-]Unknow Error!"[:-1]
        else :
            print loginInfo
