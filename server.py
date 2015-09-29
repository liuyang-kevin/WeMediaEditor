#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
import json
from time import time

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/rjson", RJSON),
            (r"/wjson", WJSON),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("wemedia.html", settings=self.application.settings)

class RJSON(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type','application/json')
        rspd = {'status': 201, 'msg':'ok'}
        try:
            timestamp = int(time())
            post_dic = {
            }
        except:
            rspd['status'] = 500
            rspd['msg'] = '错误：提交数据出错'
            self.write(json.dumps(rspd))
            return
        result = get_article()
        
        if result:
            rspd['status'] = 200
            # rspd['msg'] = '%s' % str(result)
            rspd['msg'] = result
            self.write(json.dumps(rspd))
            return
        else:
            rspd['status'] = 500
            rspd['msg'] = '错误： 未知错误，请尝试重新提交'
            self.write(json.dumps(rspd))
            return
            
class WJSON(tornado.web.RequestHandler):
    def post(self):
        self.set_header('Content-Type','application/json')
        rspd = {'status': 201, 'msg':'ok'}
        
        try:
            timestamp = int(time())
            post_dic = {
                'content' : self.get_argument("content",""),
                'article_edit_time' : timestamp,
            }
        except:
            rspd['status'] = 500
            rspd['msg'] = '错误：提交数据出错'
            self.write(json.dumps(rspd))
            return

        result = put_article(post_dic)
        if result:
        # if True:
            rspd['status'] = 200
            rspd['msg'] = '完成： 你已经成功修改了这篇文章 %s' % str(result)
            self.write(json.dumps(rspd))
            return
        else:
            rspd['status'] = 500
            rspd['msg'] = '错误： 未知错误，请尝试重新提交'
            self.write(json.dumps(rspd))
            return

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    
def put_article(dic):
    import os,sys
    try:
        fsock = open("test.json", "w")
        fsock.write(str(dic))
        fsock.close()
        return "done"
    except:
        return None
def get_article():
    import os,sys
    article = ""
    try:
        fsock = open("test.json", "r")
        AllLines = fsock.readlines()
        #Method 1
        # for EachLine in AllLines:
#             article = article + EachLine
        fsock.close()
        # return article
        return AllLines[0]
    except:
        return None
    
    
    


if __name__ == "__main__":
    main()






# import os,sys
#
# try:
#     fsock = open("D:/SVNtest/test.py", "r")
# except IOError:
#     print "The file don't exist, Please double check!"
#     exit()
# print 'The file mode is ',fsock.mode
# print 'The file name is ',fsock.name
# P = fsock.tell()
# print 'the postion is %d' %(P)
# fsock.close()
#
# #Read file
# fsock = open("D:/SVNtest/test.py", "r")
# AllLines = fsock.readlines()
# #Method 1
# for EachLine in fsock:
#     print EachLine
#
# #Method 2
# print 'Star'+'='*30
# for EachLine in AllLines:
#     print EachLine
# print 'End'+'='*30
# fsock.close()
#
# #write this file
# fsock = open("D:/SVNtest/test.py", "a")
# fsock.write("""
# #Line 1 Just for test purpose
# #Line 2 Just for test purpose
# #Line 3 Just for test purpose""")
# fsock.close()
#
#
# #check the file status
# S1 = fsock.closed
# if True == S1:
#     print 'the file is closed'
# else:
#     print 'The file donot close'