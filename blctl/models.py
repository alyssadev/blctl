class Model:
    translations = { }
    def __init__(self, *args, **kwargs):
        self._data = kwargs
        for k,v in kwargs.items():
            if k in translations:
                if type(translations[k]) is list:
                    v = [globals()[translations[k][0]](**i) for i in v]
                else:
                    v = globals()[translations[k]](*args, **kwargs)
            setattr(self, k, v)

class TaxCode(Model):
    pass

# Account
class Account(Model):
    # https://api.binarylane.com.au/reference/#tag/Accounts
    translations = {"tax_code": "TaxCode"}

# Billing Information
class Balance(Model):
    # https://api.binarylane.com.au/reference/#tag/Customers/paths/~1v2~1customers~1my~1balance/get
    pass

class Invoice(Model):
    # https://api.binarylane.com.au/reference/#tag/Customers/paths/~1v2~1customers~1my~1invoices~1{invoice_id}/get
    translations = {"tax_code": "TaxCode", "invoice_items": ["InvoiceItem"]}

class InvoiceItem(Model):
    pass

# Servers
class Server(Model):
    # https://api.binarylane.com.au/reference/#tag/Servers/paths/~1v2~1servers~1{server_id}/get
    translations = {"region": "Region", "image": "Image", "size": "Size", "networks": "NetworkDetails", "disks": ["Disk"]}

class Region(Model):
    pass

class Image(Model):
    pass

class Size(Model):
    pass

class NetworkDetails(Model):
    translations = {"v4": "Network", "v6": "Network"}

class Network(Model):
    pass

class Disk(Model):
    pass
