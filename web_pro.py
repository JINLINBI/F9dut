#coding:utf8
#!/usr/bin/python
import urllib
import urllib2
import cookielib
import hashlib
import re
import os
import time
class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self,req,fp,code,msg,httpmsg):
        pass
#        print httpmsg.headers
#        return HTTPRedirectHandler.http_error_301(self,req,fp,code,msg,httpmsg)
    def http_error_302(self,req,fp,code,msg,httpmsg):
        pass
 #       print httpmsg.headers
 #      return HTTPRedirectHandler.http_error_302(self,req,fp,code,msg,httpmsg)

class Web_pro(object):
    def __init__(self):
        self.cookie=cookielib.CookieJar()
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.viewState=""

        urllib2.install_opener(self.opener)
    def viewPage(self,root_url):
        page=urllib2.urlopen(root_url).read()
        decodePage=unicode(page,"gb2312").encode("utf-8")
        self.viewState=self.__getView(decodePage)

    def getCode(self,code_url):
        m=hashlib.md5()
        m.update("%s%s"%(time.time(),103))
        for i in self.cookie:
            cookie=i.name+':'+i.value
        page=urllib2.urlopen(code_url).read()
        codePath="./codes/%s.gif"%m.hexdigest()
        fp=open(codePath,'wb')
        fp.write(page)
        fp.close
        return codePath
    def login(self,login_url,name,passwd,code):
        print "[+]tring %s:%s[code:%s]"%(name,passwd,code)
	postdata = urllib.urlencode({
      		'__VIEWSTATE':self.viewState,   		
      		'txtUserName':name,	#std ID
     		'TextBox2':passwd,	#password
                'txtSecretCode':code,
            	'RadioButtonList1':unicode("学生","utf8").encode("gb2312"),
                'Button1':'',
                'lbLanguage':'',
                'hidPdrs':'',
                'hidsc':''})
	headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'}
	request=urllib2.Request(login_url,postdata,headers)
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie),MyHTTPRedirectHandler)
        loginPage=None
        try:
	    socket=opener.open(request)
            loginPage=socket.read()
        except urllib2.URLError as e:
            if hasattr(e,'code'):
                error_info=e.code
            elif hasattr(e,'reason'):
                error_info=e.reason
	#loginPage=urllib2.urlopen(request).read()
        if loginPage:
	    loginInfo=unicode(loginPage,'gb2312').encode("utf-8")
            return loginInfo
        else :
            return error_info
    def getStudent(self,name):
        for i in self.cookie:
            Cookie=i.name+'='+i.value
        page=None
        try :
            request=urllib2.Request("http://jwgldx.gdut.edu.cn/xs_main.aspx?xh=%s"%name)
            request.add_header('Host','jwgldx.gdut.edu.cn')
            request.add_header('User-Agent','FireFox/45.0')
            request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            request.add_header('Accept-Language','en-US,en:q=0.5')
            request.add_header('Accept-Encoding','gzip,deflate')
            request.add_header('Referer','http://jwgldx.gdut.edu.cn/default2.aspx')
            request.add_header('Cookie',Cookie)
            socket=urllib2.urlopen(request)
            page=socket.read()
        except urllib2.URLError as e:
            if hasattr(e,'code'):
                error_info=e.code
            elif hasattr(e,'reason'):
                error_info=e.reason
        if page:
            decodePage=unicode(page,'gb2312').encode('utf-8')
            return decodePage
        else :
            return error_info
    def __getView(self,Page):
        view=r'name="__VIEWSTATE" value="(.+)" '
        view=re.compile(view)
        return view.findall(Page)[0]
