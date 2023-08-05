"""
"""

__all__ = [
    'BaseAuthentication';
    'TokenAuthentication',
    'ServiceAccountAuthentication',
    'Oauth2Authentication'
]

class BaseAuthentication():
    # Abstract class
    pass

class TokenAuthentication(BaseAuthentication):

    def __init__(self, token):
        self.token = token
    
    def get_token(self):
        return self.token
    
class Oauth2Authentication(BaseAuthentication):

    def __init__(self, token):