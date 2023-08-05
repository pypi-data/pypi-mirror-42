import uuid

from traitlets import Bool
from tornado import gen

from jupyterhub.auth import Authenticator
from jupyterhub.handlers import BaseHandler
from jupyterhub.utils import url_path_join

# import re
# from base64 import b32encode, b32decode
'''
from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.auth import LocalAuthenticator
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import List
'''
# from traitlets import Unicode
# from ast import literal_eval

'''
def safeinput_encode(input_str):
    """
    :param input_str: string
    :return: b32encoded utf-8 string with stripped padding equals
    """
    encoded_str = str(b32encode(bytes(input_str, 'utf-8')), 'utf-8')
    return encoded_str.replace('=', '')


def safeinput_decode(input_str):
    """
    :param input_str: expects a b32encoded utf-8 string
    :return: a decoded utf-8 string
    """
    # Encoder removed "=" padding to satisfy validate_input
    # Pad with "="" according to:
    # https://tools.ietf.org/html/rfc3548 :
    # (1) the final quantum of encoding input is an integral multiple of 40
    # bits; here, the final unit of encoded output will be an integral
    # multiple of 8 characters with no "=" padding.
    if len(input_str) % 8 != 0:
        padlen = 8 - (len(input_str) % 8)
        padding = "".join('=' for i in range(padlen))
        decode_str = "{}{}".format(input_str, padding)
    else:
        decode_str = input_str

    return str(b32decode(bytes(decode_str, 'utf-8')), 'utf-8')
'''

'''
def extract_headers(request, headers):
    user_data = {}
    for _, header in enumerate(headers):
        value = request.headers.get(header, "")
        if value:
            try:
                user_data[header] = value
            except KeyError:
                pass
    return user_data


class PartialBaseURLHandler(BaseHandler):
    """
    Fix against /base_url requests are not redirected to /base_url/home
    """
    @web.authenticated
    @gen.coroutine
    def get(self):
        self.redirect(url_path_join(self.hub.server.base_url, 'home'))


class RemoteUserLogoutHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        user = self.get_current_user()
        if user:
            self.clear_login_cookie()
        self.redirect(self.hub.server.base_url)


class RemoteUserLoginHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        """ login user """
        self.log.info(f"self.get_current_user() -> "
                      f"{self.get_current_user()}")
        if self.get_current_user() is not None:
            self.log.info(
                f"User: {self.get_current_user()}:"
                f"{self.get_current_user().name} is already authenticated")
            self.redirect(url_path_join(self.hub.server.base_url, 'home'))
        else:
            user_auth = extract_headers(self.request,
                                        self.authenticator.header_names)
            # for item in self.authenticator.header_names:
            #    if item not in user_auth:
            #        raise web.HTTPError(401,
            #                            "You are not Authenticated to do this")
            yield self.login_user(user_auth)

            argument = self.get_argument("next", None, True)
            self.log.info(f"argument prepare -> {argument}")
            if argument is not None:
                self.log.info(f"redirect argument -> {argument}")
                self.redirect(argument)
            else:
                self.log.info(
                    f"redirect home -> "
                    f"{url_path_join(self.hub.server.base_url, 'home')}")
                self.redirect(url_path_join(self.hub.server.base_url, 'home'))


class RemoteUserAuthenticator(Authenticator):
    """
    Accept the authenticated user name from the Remote-User HTTP header.
    """
    header_names = List(
        default_value=['Remote-User', 'Encr-Key'],
        config=True,
        help="""HTTP headers to inspect for the username and encryption key"""
    )

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
            (r'/logout', RemoteUserLogoutHandler)
        ]

    @gen.coroutine
    def authenticate(self, handler, data):
        self.log.info(f"data auth -> {data}")
        self.log.info(f"self.header_names auth -> {self.header_names}")
        for item in self.header_names:
            if item not in data:
                self.log.info(f"A '{item}' header is required"
                              f" for authentication")
                return None

        # data['Remote-User'] should be the key which contains
        # the encrypted username
        # data['Encr-Key'] should be the key which contains
        # the key to decrypt the real username
        user = {
            'name': data['Remote-User'],
            'auth_state': {
                'encryption-key': data['Encr-Key']
            }
        }
        self.log.info(f"Authenticating: {user['name']} - Login")
        return user


class RemoteUserLocalAuthenticator(LocalAuthenticator):
    """
    Accept the authenticated user name from the Remote-User HTTP header.
    Derived from LocalAuthenticator for use of features such as adding
    local accounts through the admin interface.
    """
    header_names = List(
        default_value=['Remote-User', 'Encr-Key'],
        config=True,
        help="""HTTP headers to inspect for the username and encryption key"""
    )

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
            (r'/logout', RemoteUserLogoutHandler)
        ]

    @gen.coroutine
    def authenticate(self, handler, data):
        self.log.info(f"data auth -> {data}")
        self.log.info(f"self.header_names auth -> {self.header_names}")
        for item in self.header_names:
            if item not in data:
                self.log.info(f"A '{item}' header is required"
                              f" for authentication")
                return None

        # data['Remote-User'] should be the key which contains
        # the encrypted username
        # data['Encr-Key'] should be the key which contains
        # the key to decrypt the real username
        user = {
            'name': data['Remote-User'],
            'auth_state': {
                'encryption-key': data['Encr-Key']
            }
        }
        self.log.info("Authenticated: {} - Login".format(user))
        return user
'''


class RemoteUserLoginHandler(BaseHandler):
    """
    Handler for /tmplogin
    Creates a new user with a random UUID, and auto starts their server
    """

    def initialize(self, force_new_server, process_user):
        super().initialize()
        self.force_new_server = force_new_server
        self.process_user = process_user

    @gen.coroutine
    def get(self):
        raw_user = self.get_current_user()
        if raw_user:
            if self.force_new_server and raw_user.running:
                # Stop user's current server if it is running
                # so we get a new one.
                status = yield raw_user.spawner.poll_and_notify()
                if status is None:
                    yield self.stop_single_user(raw_user)
        else:
            username = str(uuid.uuid4())
            raw_user = self.user_from_username(username)
            self.set_login_cookie(raw_user)
        user = yield gen.maybe_future(self.process_user(raw_user, self))
        self.redirect(self.get_argument("next", user.url))


class RemoteUserAuthenticator(Authenticator):
    """
    JupyterHub Authenticator for use with tmpnb.org
    When JupyterHub is configured to use this authenticator, visiting the home
    page immediately logs the user in with a randomly generated UUID if they
    are already not logged in, and spawns a server for them.
    """

    auto_login = True
    login_service = 'tmp'

    force_new_server = Bool(
        False,
        help="""
        Stop the user's server and start a new one when visiting /hub/tmplogin
        When set to True, users going to /hub/tmplogin will *always* get a
        new single-user server. When set to False, they'll be
        redirected to their current session if one exists.
        """,
        config=True
    )

    def process_user(self, user, handler):
        """
        Do additional arbitrary things to the created user before spawn.
        user is a user object, and handler is a TmpAuthenticateHandler object
        Should return the new user object.
        This method can be a @tornado.gen.coroutine.
        Note: This is primarily for overriding in subclasses
        """
        return user

    def get_handlers(self, app):
        # FIXME: How to do this better?
        extra_settings = {
            'force_new_server': self.force_new_server,
            'process_user': self.process_user
        }
        return [
            ('/tmplogin', RemoteUserLoginHandler, extra_settings)
        ]

    def login_url(self, base_url):
        return url_path_join(base_url, 'tmplogin')


'''
class DataRemoteUserAuthenticator(RemoteUserAuthenticator):
    """
    An Authenticator that supports dynamic header information
    """

    auth_headers = List(
        default_value=['Remote-User'],
        config=True,
        help="""List of allowed HTTP headers to get from user data"""
    )

    data_headers = List(
        default_value=[],
        config=True,
        help="""List of allowed data headers"""
    )

    # These paths are an extension of the prefix base url e.g. /dag/hub
    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
            (r'/logout', RemoteUserLogoutHandler),
            (r'/data', DataHandler),
        ]

    @gen.coroutine
    def authenticate(self, handler, data):
        if 'Remote-User' not in data:
            self.log.info("A Remote-User header is required")
            return None

        # Login
        real_name = data['Remote-User'].lower()
        # Make it alphanumeric
        pattern = re.compile(r'[\W_]+', re.UNICODE)
        real_name = pattern.sub('', real_name)
        encoded_name = safeinput_encode(real_name)

        user = {
            'name': encoded_name,
            'auth_state': {
                'real_name': real_name
            }
        }
        self.log.info("Authenticated: {} - Login".format(user))
        return user

    @gen.coroutine
    def pre_spawn_start(self, user, spawner):
        """Pass upstream_token to spawner via environment variable"""
        auth_state = yield user.get_auth_state()
        if not auth_state:
            # auth_state not enabled
            return

        if isinstance(auth_state, dict) and 'real_name' in auth_state:
            user.real_name = auth_state['real_name']
            self.log.debug("Pre-Spawn: {} set user real_name {}".format(
                user, user.real_name))
'''
