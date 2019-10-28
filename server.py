
import tornado.web
import tornado.httpserver
import tornado.httpclient

import io, os, json
import secrets, random

import chef
from chef import accounts

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        # internal method: does not directly return data to frontend
        auth_token = self.get_cookie('auth_token')
        if not auth_token:
            query = {
                'status': 'error',
                'msg': 'User is not logged in',
                'user': None
            }
            # how shouled this be handled?
            # raise error or pass error message to caller
            # if so, allers will have to check that they've gootten back an actual user
            return query['user']
        query = {
            'status': 'success',
            'msg': 'User is logged in',
            'user': accounts.get_account(auth_token)
        }
        return query['user']
    
class IndexPage(BaseHandler):
    def get(self):
        user = self.get_current_user()
        self.render('index.html', user=user)

class AboutPage(BaseHandler):
    def get(self):
        user = self.get_current_user()
        self.render('about.html', user=user)

class SignupPage(BaseHandler):
    def get(self):
        self.render('signup.html')
    
    def post(self):
        username = self.get_argument('username', '')
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')

        auth_status = accounts.create_account(username, email, password)
        self.write(json.dumps(auth_status))

class LoginPage(BaseHandler):
    def get(self):
        self.render('login.html')
    
    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        auth_status = accounts.confirm_account(username, password)
        self.write(json.dumps(auth_status))


from tornado.options import define
define("port", default=3312, type=int)

handlers = [
    (r"/", IndexPage),
    (r"/about", AboutPage),
    (r"/signup", SignupPage),
    (r"/login", LoginPage)
]

# switch debug mode on or off
try:
    var = os.environ['APP_STAGE']
    prod = True if var == 'PROD' else False
except:
    prod = False


settings = dict(
    debug = False if prod else True,
    cookie_secret = secrets.token_hex(16),
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    autoescape = None,
)

app = tornado.web.Application(handlers, **settings)
def start():
    try:
        tornado.options.parse_command_line()
        port = tornado.options.options.port
        server = tornado.httpserver.HTTPServer(app)
        server.listen(port)
        
        start_msg = f"App server started. Port {port}"
        print('\n' + '=' * len(start_msg) + '\n' \
            + start_msg + '\n' + '=' * len(start_msg))
        
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        stop_msg = "Stopping app server"
        print('\n' + '=' * len(stop_msg) + '\n' \
            + stop_msg + '\n' + '=' * len(stop_msg))
        import sys
        sys.exit()

if __name__ == "__main__":
    start()
