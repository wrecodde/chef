
import tornado.web
import tornado.httpserver
import tornado.httpclient

import io, os, json
import secrets, random

import chef
from chef import accounts, gallery

class BaseHandler(tornado.web.RequestHandler):
    pass

class APIHandler(tornado.web.RequestHandler):
    def get_auth_token(self):
        # token should be in POST request body
        token = self.get_argument('auth_token')
        if token is not None:
            return token
        else:
            # try getting auth_token from cookie
            # if that fails, return None
            return self.get_cookie('auth_token', None)
    
class IndexPage(BaseHandler):
    def get(self):
        self.render('index.html')

class AboutPage(BaseHandler):
    def get(self):
        self.render('about.html')

class SignupPage(BaseHandler):
    def get(self):
        self.render('signup.html')

class LoginPage(BaseHandler):
    def get(self):
        self.render('login.html')

class GalleryPage(BaseHandler):
    def get(self):
        self.render('gallery.html')
    
    def post(self):
        # processor for media file (pictures) upload
        pass

# the following handlers are strictly related with the api
class UserSignupEP(APIHandler):
    def post(self):
        username = self.get_argument('username', '')
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')

        status = accounts.create_account(username, email, password)
        self.write(status)

class UserLoginEP(APIHandler):
    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        status = accounts.confirm_account(username, password)
        self.write(status)

class FetchUserEP(APIHandler):
    def post(self):
        # auth token must be provided in request body
        auth = self.get_auth_token()
        if not auth:
            resp = {
                'status': 'error',
                'msg': 'Authentication credentials not provided',
            }
            self.write(resp)
            return
        
        account = accounts.get_account(auth)
        if not account:
            resp = {
                'status': 'error',
                'msg': 'Invalid credentials provided',
            }
            self.write(resp)
            return
            
        resp = {
            'status': 'success',
            'data': {
                'username': account.username,
                'email': account.email,
                'auth_token': account.auth_token,
            },
        }
        self.write(resp)

from tornado.options import define
define("port", default=3312, type=int)

handlers = [
    (r"/", IndexPage),
    (r"/about", AboutPage),
    (r"/signup", SignupPage),
    (r"/login", LoginPage),
    (r"/gallery", GalleryPage),
    # api endpoints
    (r"/api/v1/signup", UserSignupEP),
    (r"/api/v1/login", UserLoginEP),
    (r"/api/v1/user", FetchUserEP),
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
