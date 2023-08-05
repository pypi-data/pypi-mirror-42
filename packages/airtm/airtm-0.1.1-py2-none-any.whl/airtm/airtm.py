"""
AirTM Python SDK
This is a python module to ease integration between python apps and the AirTM API. 
"""

import requests
import logging
import urllib3
import requests
import json
import ssl
from pkg_resources import get_distribution, DistributionNotFound

class APIError(Exception):
    def __init__(self, code, value):
        self.code = code
        self.value = value
    def __str__(self):
        return repr(self.value)

class Partner:
    def __init__(self, dict = None):
        if dict:
            for k in ['currency','balance','email','name','id']:
                if k in dict:
                    setattr(self,k,dict[k])

class Operation(object):
    def __init__(self, d = None):
        self.id = None
        if isinstance( d , list):
            d = d[0]
        if d:
            for k in ['partner_id','airtm_user_id','airtm_user_email','airtm_operation_id','id','status','code','description','amount','created_at','updated_at','cancel_uri','confirmation_uri','operation_type']:
                if k in d and d[k] is not None:
                    setattr(self,k,d[k])
    def __repr__(self):
        if self.id is None:
            id = 'No ID'
        else:
            id = 'xxxx-' + self.id[-6:]
        return '{}({!r},{!r},{!r},{!r},{!r})'.format(
            self.__class__.__name__,id,self.operation_type, self.description, self.amount, self.status)

class Purchase(Operation):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.itemized_list = []

    def __repr__(self):
        if self.id is None:
            id = 'No ID'
        else:
            id = 'xxxx-' + self.id[-6:]
        return '{}({!r},{!r},{!r},{!r})'.format(
            self.__class__.__name__,id,self.operation_type, self.description, self.amount)

    def add_item(self, desc, amount, quant):
        i = {
            'description' : desc,
            'amount' : amount,
            'quantity' : quant
            }
        self.itemized_list.append(i)
        self.amount = self.calculate_total()

    def calculate_total(self):
        sum = 0
        for i in self.itemized_list:
            sum = sum + float(i['amount'])
        return float(sum)

    def to_json(self):
        params = {
            "code": self.code,
            "amount": self.amount, 
            "description": self.description,
            "redirect_uri": self.redirect_uri,
            "cancel_uri": self.cancel_uri,
            "items": self.itemized_list
        }
        return params

class Payout(Operation):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def to_json(self):
        params = {
            "amount": self.amount, 
            "description": self.description,
            "email": self.email,
            "confirmation_uri": self.confirmation_uri
        }
        return params
    
class AirTM:
    """
    Use this SDK to simplify interaction with the AirTM API
    """
    
    def __init__(self, id, secret, host, db = False):
        self.partner_id = id
        self.partner_secret = secret
        self.host    = host
        self.debug   = db
        self.version = get_distribution('AirTM').version
        self.session = requests.Session()
        self.useragent = 'airtm-python-sdk/' + self.version
        self.headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'User-Agent': self.useragent
            }
        self.__init_logging()

    def _debug(self, s):
        if self.debug:
            print(s)

    def checkout_url(self, id):
        return 'https://' + self.host + "/checkout/" + id

    def get_me(self):
        data = self.__get('/partners/me')
        p = Partner( data )
        return p

    def get_operations(self, page = 1, perPage = 10, optype = 'all'):
        """
        This does not return the items in a purchase.
        Response:
        {
           'perPage': 50, 
           'from': 1, 
           'lastPage': 1, 
           'to': 1, 
           'currentPage': 1,
           'total': 1,
           'purchases': Purchase[],
        }
        """
        url = '/operations?page=' + str(page) + '&perPage=' + str(perPage);
        if optype != 'all':
            if optype == "purchase" or optype == "payout":
                url += "&type=" + optype
            else:
                raise APIError( undefined, "Unknown operation type" )

        data = self.__get( url )
        ops = []
        for k in data['data']:
            o = Operation(k)
            ops.append(o)
        del data['data']
        data['operations'] = ops
        return data

    def get_operation(self, id):
        """
        Return an Operation object corresponding to the id provided.
        """
        self._debug("Getting operation (with id: " + id + ")...")
        data = self.__get('/operations/' + id)
        o = Operation(data)
        return o

    def create_purchase(self, purchase):
        """
        Return a new Purchase object generated from the response. This does not modify
        or augment the passed in purchase with more data. 
        """
        self._debug("Creating purchase...")
        data = self.__post('/purchases',purchase.to_json(),"json")
        new_purchase = Purchase( data )
        return new_purchase

    def create_payout(self, payout):
        """
        Return a new Payout object generated from the response. This does not modify
        or augment the passed in payout with more data. 
        """
        self._debug("Creating payout to "+ payout.email +"...")
        data = self.__post('/payouts',payout.to_json(),"json")
        new_payout = Payout( data )
        return new_payout

    def commit_payout(self, id):
        """
        Commits a payout corresponding to the id provided.
        """
        self._debug("Committing payout (with id: " + id + "...")
        data = self.__post('/payouts/' + id + '/commit',"","raw")
        p = Payout(data)
        return p

    def refund_purchase(self, id):
        """
        Refunds a purchase corresponding to the id provided.
        """
        self._debug("Refunding purchase (with id: " + id + "...")
        data = self.__post('/purchases/' + id + '/refund',"","raw")
        p = Purchase(data)
        return p


    """
    HELPER FUNCTIONS
    """
    def __init_logging(self):
        if self.debug:
            # Enabling debugging at http.client level (requests->urllib3->http.client)
            # you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
            # the only thing missing will be the response.body which is not logged.
            try: # for Python 3
                from http.client import HTTPConnection
            except ImportError:
                from httplib import HTTPConnection
            HTTPConnection.debuglevel = 1

            logging.basicConfig() # you need to initialize logging, otherwise you will not see anything from requests
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def __get(self, uri):
        """
        """
        url = 'https://' + self.host + uri

        # You're ready to make verified HTTPS requests.
        try:
            self.session.auth = ( self.partner_id, self.partner_secret )
            #self.headers['Content-type'] = "application/json"
            response = self.session.get(url, headers=self.headers)

        except requests.exceptions.SSLError as e:
            # Handle incorrect certificate error.
            self._debug("Failed certificate check: " + str(e))
            exit()

        self._debug("Response type: " + response.headers["Content-Type"])
        if response.headers["Content-Type"] == "text/plain":
            # Do something
            data = response.text
        else:
            data = json.loads(response.text)

        if response.status_code != requests.codes.ok:
            self._debug("An error was returned from the server. Throwing exception.")
            raise APIError( response.status_code, data['message'] )

        return data


    def __post(self, uri, params, format = "raw"):
        """
        This is a private helper method for performing HTTP POST requests.
        """
        url = 'https://' + self.host + uri

        try:
            self.session.auth = ( self.partner_id, self.partner_secret )
            if (format == "raw"):
                response = self.session.post(url, data=params, headers=self.headers)
            elif (format == "json"):
                self.headers['Content-type'] = "application/json"
                if params:
                    params_json = json.dumps(params)
                else:
                    params_json = None
                response = self.session.post(url, data=params_json, headers=self.headers)

        except requests.exceptions.SSLError as e:
            # Handle incorrect certificate error.
            self._debug("Failed certificate check: " + str(e))
            exit()

        if "application/json" in response.headers["Content-Type"]:
            data = json.loads(response.text)
        else:
            self._debug("Non-JSON response detected. Server is probably throwing an error.")
        
        if response.status_code != requests.codes.ok:
            self._debug("Error detected in response.")
            print "Response text: " + response.text
            if "text/plain" in response.headers["Content-Type"]:
                msg = response.text
            elif 'messages' in data and data['messages']:
                msg = data['messages']['code'][0]
            elif 'message' in data and data['message']:
                msg = data['message']

            self._debug("An error was returned from the server. Throwing exception.")
            raise APIError( response.status_code, msg )

        return data
