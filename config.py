import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '345435dsmd.35##3f90ec8062a9e91707e70c2edb919f7e8236ddb5'
    CLIENT_ID = os.environ.get('CLIENT_ID') or '8_f3OeYk3Xet1hRoUrq2qQ'
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET') or 'IBcbN6KYSxCQp7GOwRKkdRJ1087wosdTbrjKHgif31voikQXzXNxwCxnYs1anCtt'
    GOOGLEMAPS_KEY = os.environ.get('GOOGLEMAPS_KEY') or 'AIzaSyDPIxQ95g3W-PAd0WPy_PjM84-HtAKQp1U'
    FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID') or '426344891059039'
    FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET') or 'a9afa0f63af2cbc8385f7daaa9ca21dc'
