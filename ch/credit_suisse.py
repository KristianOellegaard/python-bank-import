import csv
from bank_backends.base import BaseBankBackend
from decimal import Decimal
import datetime
from django.utils.encoding import smart_unicode

class CreditSuisseBackend(BaseBankBackend):
    title = "Credit Suisse (EN)"

    def handle_file(self):
        csvReader = csv.reader(self.file, delimiter=',', quotechar='\"')
        has_data = False
        for row in csvReader:
            if len(row) != 6:
                has_data = False
            if has_data:
                self.handle_line(row)
            if row == ['Booking Date', 'Text', 'Debit', 'Credit', 'Value Date', 'Balance']:
                has_data = True


    def handle_line(self, line):
        booking_date, text, debit, credit, date, balance = line
        if not debit:
            debit = 0
        if not credit:
            credit = 0
        if date:
            date = datetime.datetime.strptime(date, "%d.%m.%Y")
        if balance:
            balance = Decimal(balance)
        else:
            balance = None
        transaction_value = Decimal(credit) - Decimal(debit)
        text = u"%s" % smart_unicode(text.decode('iso-8859-1'))
        text = unicode(text)
        self.save_transaction(date=date, value=transaction_value, balance=balance, text=text)