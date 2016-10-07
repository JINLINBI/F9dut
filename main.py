#coding:utf8
#!/usr/bin/python
import code_pro
import web_pro
import getpass
class Main(object):
    def __init__(self):
        self.code_pro=code_pro.Code_pro()
        self.web_pro=web_pro.Web_pro()

if __name__=='__main__':
    root_url="http://jwgldx.gdut.edu.cn"
    login_url="http://jwgldx.gdut.edu.cn/default2.aspx"
    code_url="http://jwgldx.gdut.edu.cn/CheckCode.aspx"
    #name=raw_input("Please Input Your Student Id:")
    passwd=getpass.getpass("Please Input Your Password:")
    name=3114002780
    main=Main()
    main.web_pro.viewPage(root_url)
    codePath=main.web_pro.getCode(code_url)
    code=main.code_pro.crackCode(codePath)
    loginInfo=main.web_pro.login(login_url,name,passwd,code)
    if loginInfo !=302:
        print loginInfo
    else :
        page=main.web_pro.getStudent(name)
        print page


