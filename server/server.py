import tornado.web, tornado.ioloop
import motor

HTML_LOCATION="./html"

DEMO_USER={
    "phone": "",
    "address": "",
    "status":0
    }

DEMO_AYI=[
    {
        "name": "",
        "phone": "",
        "area": ""
        },
    {
        "name": "",
        "phone": "",
        "area": ""
        }
    ]

SMS={
    "url": "https://api.twilio.com/2010-04-01/Accounts/AC722b329f84edafadeafc17fe613ada80/SMS/Messages.json",
    "user": "AC722b329f84edafadeafc17fe613ada80",
    "pass": "8b9d56af64c029abfeccf1af0f23bd9c",
    }

class FindHandler(tornado.web.RequestHandler):
    def sms(self):
        pass

#        request = tornado.httpclient.HTTPRequest(url=url,
#                                                 method='POST',
#                                                 body=body,
#                                                 validate_cert=False)

    @tornado.web.asynchronous
    def post(self):
        """Finding an Ayi
        """
        position = self.get_argument('position')
        

        response = {
            'status': "OK"
            }
        DEMO_USER["status"] = 1
        self.write(response)

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
        (r'/', PageHandler)
    ],
#    db=db
)

if __name__ == "__main__":
    print 'Starting ...'
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
