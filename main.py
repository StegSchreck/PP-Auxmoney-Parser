#!/usr/bin/env python
import argparse

import file_impex
from auxmoney import Auxmoney


def main():
    args = parse_args()
    auxmoney = Auxmoney(args)
    loan_transactions = auxmoney.parse_loans()
    file_impex.save_loan_transactions_to_csv(loan_transactions)
    auxmoney.browser_handler.kill()


def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-v", "--verbose", action="count", help="increase output verbosity", required=False)
    argparser.add_argument("-x", "--show_browser", help="show the browser doing his work", action="store_true",
                           required=False)
    argparser.add_argument("-u", "--username", help="Username for Auxmoney login", required=True)
    argparser.add_argument("-p", "--password", help="Password for Auxmoney login", required=True)
    args = argparser.parse_args()
    return args


if __name__ == "__main__":
    main()
