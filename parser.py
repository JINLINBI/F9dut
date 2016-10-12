#coding:utf8
#!/usr/bin/python
from bs4  import BeautifulSoup
import re
class Parser(object):
    def __init__(self):
        pass
    def parserError(self,page):
        #soup=BeautifulSoup(page,'html.parser',from_encoding='utf-8')
        #error=soup.find_all('')
        #vertify=re.search(r'id',page)
        vertify=re.search(r'验证码不正确',page)
        passError=re.search(r'密码',page)
        user=re.search(r'用户名不存在',page)
        if vertify is not None:
            return 444
        elif user is not None:
            return 555
        elif passError is not None:
            return 666
    def parserName(self,page):
        soup=BeautifulSoup(page,'html.parser',from_encoding='utf-8')
        name=soup.find_all('span',id=re.compile('xhxm'))
        return name[0].text
if __name__=='__main__':
    page="<span id='xhxm'>长进用同学欢迎</span><script>alert('验证码不正确')</scritp>"
    parser=Parser()
    name=parser.parserName(page)
    print name#    error=parser.parserError(page)
#    print error
