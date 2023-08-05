import odoorpc

DONODOO_URL = "%s.donodoo.it"
DONODOO_TEST_URL = "127.0.0.1"



class DonodooResource(object):
    _obj = None

    VALID_METHODS = [
        'search',
        'search_read',
        'browse',
        'unlink',
        'create',
        'write'
    ]

    def __init__(self, odoo):
        self.odoo = odoo

    def __getattr__(self, name):
        def call_odoo(*args, **kwargs):
            method = getattr(self.odoo.env[self._obj], name)
            return method(*args, **kwargs)

        if name not in self.VALID_METHODS:
            raise Exception("Method '%s' not found" % name)
        return call_odoo

class DonorsResource(DonodooResource):
    _obj = 'ngo.donor'

class SubscriptionsResource(DonodooResource):
    _obj = 'sale.subscription'

class JobsResource(DonodooResource):
    _obj = 'ngo.job'

class CampaignsResource(DonodooResource):
    _obj = 'ngo.campaign'

class Donodoo(object):
    def __init__(self, domain, email, password, port=80, database="", test=False, url=''):
        if not url:
            url = DONODOO_URL % domain if not test else DONODOO_TEST_URL

        if not test:
            url = DONODOO_URL % domain if not url else url
            port = 443
            self.odoo = odoorpc.ODOO(url, port=port, protocol='jsonrpc+ssl')
        else:
            url = DONODOO_TEST_URL % domain if not url else url
            self.odoo = odoorpc.ODOO(url, port=port)

        if not database:
            database = "odoo_%s" % domain
            
        try:
            self.odoo.login(database, email, password)
        except Exception as e:
            print(e)
            raise Exception("Invalid login")
        
        self.env = self.odoo.env
        self.donors = DonodooResource(self)
        self.subscriptions = SubscriptionsResource(self)
        self.jobs = JobsResource(self)
        self.campaigns = CampaignsResource(self)
    


        