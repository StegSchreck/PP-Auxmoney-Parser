#!/usr/bin/env python
import argparse
import os
import sys

import file_impex
from auxmoney import Auxmoney

EXPORTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'exports'))


def main():
    args = parse_args()
    auxmoney = Auxmoney(args)
    loan_transactions = auxmoney.parse_loans()
    print_summary(loan_transactions)
    file_impex.save_loan_transactions_to_csv(loan_transactions, folder=args.destination)
    auxmoney.browser_handler.kill()


def print_summary(loan_transactions):
    interests = [transaction['value'] for transaction in loan_transactions if transaction['type'] == 'Zinsen']
    fees = [transaction['value'] for transaction in loan_transactions if transaction['type'] == 'Gebühren']

    if len(interests) <= 0 or len(fees) <= 0:
        return
    avg_interest = sum(interests) / float(len(interests))
    avg_fee = sum(fees) / float(len(fees))

    sys.stdout.write('===== SUMMARY =====\r\n')
    sys.stdout.write('{count} transactions of interests: SUM={sum} AVG={avg} MIN={min} MAX={max}\r\n'
                     .format(count=len(interests), sum=sum(interests), avg=avg_interest, min=min(interests), max=max(interests)))
    sys.stdout.write('{count} transactions of fees: SUM={sum} AVG={avg} MIN={min} MAX={max}\r\n'
                     .format(count=len(fees), sum=sum(fees), avg=avg_fee, min=min(fees), max=max(fees)))
    sys.stdout.write('===================\r\n\r\n')
    sys.stdout.flush()


def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-v", "--verbose", action="count", help="increase output verbosity", required=False)
    argparser.add_argument("-x", "--show_browser", help="show the browser doing his work", action="store_true",
                           required=False)
    argparser.add_argument("-u", "--username", help="username for Auxmoney login", required=True)
    argparser.add_argument("-p", "--password", help="password for Auxmoney login", required=True)
    argparser.add_argument("--earliest", help="earliest date of transactions to be considered", required=False)
    argparser.add_argument("--latest", help="latest date of transactions to be considered", required=False)
    argparser.add_argument("-d", "--destination", help="destination folder for result CSV file", required=False,
                           default=EXPORTS_FOLDER)
    args = argparser.parse_args()
    return args


if __name__ == "__main__":
    main()
