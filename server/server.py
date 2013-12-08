import tornado
from tornado import httpclient
import tornado.web, tornado.ioloop
import motor

HTML_LOCATION="./html"

DEMO_USER={
    "phone": "",
    "address": "",
    "status": 0,
    }

DEMO_AYI={
    "0": {
        "name": "ayi1",
        "phone": '%2B15612576060',
        "area": "haidian"
        },
    "1": {
        "name": "",
        "phone": "",
        "area": ""
        }
    }

SMS={
    "url": "https://api.twilio.com/2010-04-01/Accounts/AC46a06d1e1dfbfb6883d7ab83a428d8bd/SMS/Messages.json",
    "user": "AC46a06d1e1dfbfb6883d7ab83a428d8bd",
    "pass": "ab9841276591d840e4e089858e981bd8",
    'from': '%2B18565170283',
    }

class FindHandler(tornado.web.RequestHandler):
    def sms(self, to):
        try:
            with open("%s/text_ayi.txt"%(HTML_LOCATION), 'r') as content_file:
                content = content_file.read()
        except:
            content="Beijing, Shuangjing, Fulichen, Buildinf A2, Apt 3456 - Today at 4:00PM - Thank you!"
        body="To=%s&From=%s&Body=%s"%(to,SMS['from'],content)
        print "body='%s'"%body

        request = httpclient.HTTPRequest(url=SMS['url'],
                                         method='POST',
                                         body=body,
                                         validate_cert=False,
                                         auth_username=SMS['user'],
                                         auth_password=SMS['pass'])
        http_client = httpclient.HTTPClient()
        try:
            response = http_client.fetch(request)
            print response.body
        except httpclient.HTTPError as e:
            print "Error:", e
        http_client.close()

#    @tornado.web.asynchronous
#    def post(self):
#        """Finding an Ayi
#        """
#        position = self.get_argument('position')
#        
#        response = {
#            'status': "OK"
#            }
#        DEMO_USER["status"] = 1
#        self.write(response)

    @tornado.web.asynchronous
    def get(self):
        """Finding an Ayi - get debug
        """
        self.sms(DEMO_AYI["0"]["phone"])
        DEMO_USER["status"] = 1
        response = {
            'status': DEMO_USER["status"]
            }
        self.write(response)
        self.finish()

#    def _on_response(self, result, error):
#        if error:
#            raise tornado.web.HTTPError(500, error)
#        else:
#            self.redirect('/')

class StatusHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
#    def post(self):
    def get(self):
        """Getting status
        """
        #id = self.get_argument('id')
        response = {
            'status': DEMO_USER.get("status",0)
            }
        self.write(response)
        self.finish()

# debug only
class CancelHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        """Cancel curent order (debug only)
        """
        DEMO_USER["status"] = 0
        response = {
            'status': DEMO_USER.get("status",0)
            }
        self.write(response)
        self.finish()

class AnswerHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        """Got answer from Ayi
        """
        print "body='%s'"%(self.request.body)
        try:
            answer = int(self.get_argument('Body'))
        except:
            print "error parsing answer"
            answer = 1
        
        DEMO_USER["status"] = (2 if answer == 1 else 3)
        response = {
            'status': DEMO_USER.get("status",2)
            }
        self.write(response)
        self.finish()

class PageHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        """Display Homepage
        """
        with open("%s/index.html"%(HTML_LOCATION), 'r') as content_file:
            content = content_file.read()
        self.write(content)
        self.finish()

#db = motor.MotorClient().open_sync().maideasy

application = tornado.web.Application(
    [
        (r'/api/find', FindHandler),
        (r'/api/status', StatusHandler),
        (r'/api/cancel', CancelHandler),
        (r'/api/answer', AnswerHandler),
        (r'/', PageHandler)
    ],
#    db=db
)

if __name__ == "__main__":
    print 'Starting ...'
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
