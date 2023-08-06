# -*- coding: utf-8 -*-
import urllib3,json
urllib3.disable_warnings()

class CJApi:
    def __init__(self,yourTonken):
        self.token=yourTonken
    
    #post request
    def post(self,url,params):
        http=urllib3.PoolManager()
        resp=http.request(
            "POST",
            "https://developers.cjdropshipping.com/%s" % url,
            body=json.dumps(params).encode('utf-8'),
            headers={
                'Content-Type':'application/json',
                'CJ-Access-Token':self.token
            }
        )
        return resp
