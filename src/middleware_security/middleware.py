# -*- coding: utf-8 -*-
import requests
from falcon_exceptions import HTTPException
from requests.exceptions import HTTPError

class Security(object):

    def __init__(self, config):
        self.config = config

    def process_request(self, req, resp):
        try:
            if req.method == 'OPTIONS':
                return

            with requests.Session() as s:
                s.trust_env = False
                r = s.get('%s/%s' % (self.config["api"], 'verify_token'),
                    headers={'Authorization': req.auth}
                )
                r.raise_for_status()

                data = r.json()
                req.context["token_user"] = data["token"]["user"]
                req.context["token_roles"] = data["token"]["roles"]
        except HTTPError as e:
            status_code = r.status_code or 500
            raise HTTPException(status_code)
        except Exception as e:
            raise HTTPException(401)
