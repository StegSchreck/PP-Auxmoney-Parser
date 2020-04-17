import datetime
import os
import sys
import time

TIMESTAMP = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
EXPORTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'exports'))
CSV_HEADER = 'Datum,Wert,Buchungswährung,Typ,Notiz\n'


def save_loan_transactions_to_csv(loan_interests, folder=EXPORTS_FOLDER, filename=TIMESTAMP + '_auxmoney.csv'):
    sys.stdout.write('===== saving loan interests to CSV\r\n')
    sys.stdout.write('      folder: {}\r\n'.format(folder))
    sys.stdout.write('      filename: {}\r\n'.format(filename))
    sys.stdout.write('      number of entries: {}\r\n'.format(len(loan_interests)))
    sys.stdout.flush()
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, filename), 'w+', encoding='UTF-8') as output_file:
        output_file.write(CSV_HEADER)
        for loan_interest_transaction in loan_interests:
            output_file.write(convert_loan_to_csv(loan_interest_transaction))


def convert_loan_to_csv(transaction):
    movie_csv = '' + transaction['date'] + ',' + \
                '"' + str(transaction['value']).replace('.', ',') + '",' + \
                'EUR,' + \
                '' + transaction['type'] + ',' + \
                '' + transaction['id'] + ',' + \
                '\n'
    return movie_csv
