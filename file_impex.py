import datetime
import os
import sys
import time

TIMESTAMP = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
CSV_HEADER = 'Datum,Wert,Buchungswährung,Typ,Notiz\n'


def save_loan_transactions_to_csv(loan_transactions, folder, filename=TIMESTAMP + '_auxmoney.csv'):
    sys.stdout.write('===== saving loan transactions to CSV\r\n')
    sys.stdout.write('      folder: {}\r\n'.format(folder))
    sys.stdout.write('      filename: {}\r\n'.format(filename))
    sys.stdout.write('      number of entries: {}\r\n'.format(len(loan_transactions)))
    sys.stdout.flush()
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, filename), 'w+', encoding='UTF-8') as output_file:
        output_file.write(CSV_HEADER)
        for transaction in loan_transactions:
            output_file.write(convert_transaction_to_csv_row(transaction))


def convert_transaction_to_csv_row(transaction):
    transaction_csv_row = '' + transaction['date'] + ',' + \
                          '"' + str(transaction['value']).replace('.', ',') + '",' + \
                          'EUR,' + \
                          '' + transaction['type'] + ',' + \
                          '' + transaction['id'] + ',' + \
                          '\n'
    return transaction_csv_row
