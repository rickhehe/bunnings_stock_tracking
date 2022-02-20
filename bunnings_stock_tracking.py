import appdaemon.plugins.hass.hassapi as hass

from csv import DictReader
from collections import defaultdict

import requests


URL = r'https://api.prod.bunnings.com.au/v1/stores/products/stock'

PRODUCTS = '/config/appdaemon/apps/bunnings_stock_tracking/products.csv'

# If you're outside Christchurch you can modify **PARAMS** to get results in your area.
PARAMS = {  # This is Christchurch
    'latitude':'-43.5784076',
    'longitude':'172.5726805',
}

class Bunnings_stock_tracking(hass.Hass):

    def initialize(self):
        self.log(f'{__name__} is now live.')

        try:
            self.run_every(
                self.stream,
                'now',
                60
            )

        except Exception as e:
            self.send_email_to(
                message=e,
                title=f'{__name__} Error'
            )

    @property
    def products(self):
    
        '''Using PRODUCTS as data source, this function returns a list of dict, with product code as key; name, and url as value.
        '''

        c = defaultdict(dict)

        with open(PRODUCTS) as f:
            reader = DictReader(f)
        
            for x in reader:
                k = x['product_code']
                x.pop('product_code')
     
                c[k]=x

        return c

    @property
    def response(self):
        '''Returns a requests response
        '''

        HEADERS = {
            'Authorization': self.args['token'],  #apps.yaml
            'clientId': self.args['clientId'],  #apps.yaml
            'country': 'NZ',
            'locale': 'en_NZ',
        }

        with requests.Session() as s:
        
            r = s.post(
                URL,
                headers=HEADERS,
                params=PARAMS,
                json={'products':list(self.products.keys())}
            )
        
        return r
        
    @property
    def stores(self):
        '''Returns a liser
        '''

        x = self.response.json()
        stores = x['data']['stores']

        return stores
    
    def send_email_to(self, title='rickhehe', message=''):
        
        self.call_service(
            'notify/send_email_to_rick_notifier',
            message=message,
            title='Bunnings',
        ) 

    def stream_stock_level(self):

        s = defaultdict(str)
        for store in self.stores:

            for product in store['products']:
                
                # Only proceed if the store has stock.
                if product['stock']['stockLevel'] > 0:
                
                    s[product['code']] += f"    {product['stock']['stockLevel']} in {store['displayName']}\n"
                
        for i in s:
            name = self.products.get(i)['name']
            url = self.products.get(i)['url']
            
            message = f"\n\n{i} {name}\n{url}\n\n{s[i]}"

            self.send_email_to(message=message)

    def stream(self, kwargs):

        self.stream_stock_level()
