# -*- coding: utf-8 -*-
import jwt
from falcon_exceptions import HTTPException

class AuthVerify(object):

    def __init__(self, config):
        self.config = config

    def process_request(self, req, resp):
        if req.method == 'OPTIONS':
            return

        if 'security' in self.config:
            secure_paths = self.config['security']['secure_paths']
            current_path = req.path

            if current_path in secure_paths:
                return

        if not req.auth:
            raise HTTPException(401, "Authorization token not send")

        bearer_token = req.auth
        bearer_token = bearer_token.split(' ')[1]

        decoded_token = jwt.decode(bearer_token, verify=False)

        req.context['token_user'] = decoded_token['user']
        req.context['token_scopes'] = decoded_token['scopes']
