import hashlib

class BaseBankBackend(object):
    """
    All bank backends should inherit from this class
    """
    file = None
    title = None
    transactions = []

    def __init__(self, file, *args, **kwargs):
        self.file = file

    @classmethod
    def identifier(cls):
        return cls.__name__

    def handle_file(self):
        pass

    def handle_line(self, line):
        pass

    def save_transaction(self, date=None, value=None, balance=None, text=None):
        hash = u"&".join([unicode(date), unicode(value), unicode(balance), text])
        self.transactions.append({
            'date': date,
            'value': value,
            'balance': balance,
            'text': text,
            'hash': hashlib.md5(hash.encode("utf-8")).hexdigest(),
        })