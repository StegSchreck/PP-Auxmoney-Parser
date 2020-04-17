import sys
import time

from selenium.common.exceptions import NoSuchElementException

from browser_handler import BrowserHandler


class Auxmoney:
    def __init__(self, args):
        self.args = args

        login_form_selector = "//form[@id='login']"
        self.LOGIN_USERNAME_SELECTOR = login_form_selector + "//input[@id='login_loginUsername']"
        self.LOGIN_PASSWORD_SELECTOR = login_form_selector + "//input[@id='login_loginPassword']"
        self.LOGIN_BUTTON_SELECTOR = login_form_selector + "//input[@type='submit']"

        self._init_browser()

    def _init_browser(self):
        self.browser_handler = BrowserHandler(self.args)
        self.browser = self.browser_handler.browser
        self.login()

    def login(self):
        self.browser.get("https://www.auxmoney.com/login")
        time.sleep(1)

        iteration = 0
        while self._user_is_not_logged_in():
            iteration += 1
            try:
                self._insert_login_credentials()
                self._click_login_button()
            except NoSuchElementException as e:
                if iteration > 10:
                    raise e
                time.sleep(iteration * 1)
                continue
            if iteration > 2:
                self._handle_login_unsuccessful()

    def _user_is_not_logged_in(self):
        return len(self.browser.find_elements_by_xpath(self.LOGIN_BUTTON_SELECTOR)) > 0 \
               and len(self.browser.find_elements_by_xpath(self.LOGIN_USERNAME_SELECTOR)) > 0 \
               and len(self.browser.find_elements_by_xpath(self.LOGIN_PASSWORD_SELECTOR)) > 0

    def _insert_login_credentials(self):
        login_field_user = self.browser.find_element_by_xpath(self.LOGIN_USERNAME_SELECTOR)
        login_field_user.clear()
        login_field_user.send_keys(self.args.username)
        login_field_password = self.browser.find_element_by_xpath(self.LOGIN_PASSWORD_SELECTOR)
        login_field_password.clear()
        login_field_password.send_keys(self.args.password)

    def _click_login_button(self):
        login_button = self.browser.find_element_by_xpath(self.LOGIN_BUTTON_SELECTOR)
        login_button.click()
        time.sleep(2)  # wait for page to load

    def _handle_login_unsuccessful(self):
        time.sleep(1)
        if self._user_is_not_logged_in():
            sys.stderr.write("Login to Auxmoney failed.")
            sys.stdout.flush()
            self.browser_handler.kill()
            sys.exit(1)

    def parse_loans(self):
        self.browser.get("https://www.auxmoney.com/anlegercockpit/projects")
        time.sleep(1)

        all_loans_transactions = []

        loan_links = self.browser.find_elements_by_xpath("//table[@class='project-list']//a[@class='details']")
        loan_details_urls = [loan_link.get_attribute('href') for loan_link in loan_links]

        if self.args and self.args.verbose and self.args.verbose >= 1:
            sys.stdout.write('      found {count} loans to parse\r\n'.format(count=len(loan_details_urls)))
            sys.stdout.flush()

        for loan_details_url in loan_details_urls:
            loan_transactions = self._parse_loan(loan_details_url)
            all_loans_transactions.extend(loan_transactions)

        return all_loans_transactions

    def _parse_loan(self, loan_details_url):
        self.browser.get(loan_details_url)
        time.sleep(2)
        loan_id = loan_details_url.split('/')[-1]

        return self._parse_loan_transactions(loan_id)

    def _parse_loan_transactions(self, loan_id):
        loan_transactions = []

        back_payment_plan_table_rows = \
            self.browser.find_elements_by_xpath("//div[@class='left-box backPaymentPlan']/table//tr")[1:]
        back_payment_table_rows = \
            self.browser.find_elements_by_xpath("//div[@class='right-box backPayment']/table//tr")[1:]

        if self.args and self.args.verbose and self.args.verbose >= 1:
            sys.stdout.write('      {id}: found {count} transactions (some might be all zero)\r\n'
                             .format(id=loan_id, count=len(back_payment_table_rows)))
            sys.stdout.flush()

        for i in range(len(back_payment_table_rows)):
            transaction_date = back_payment_plan_table_rows[i].find_elements_by_tag_name("td")[1].text

            loan_transaction = dict()
            loan_transaction['id'] = loan_id
            loan_transaction['date'] = transaction_date
            loan_transaction['value'] = float(back_payment_table_rows[i].find_elements_by_tag_name("td")[1].text
                                                                        .replace('€', '').replace(',', '.').strip())
            loan_transaction['type'] = 'Zinsen'
            if loan_transaction['value'] > 0:
                loan_transactions.append(loan_transaction)
                if self.args and self.args.verbose and self.args.verbose >= 2:
                    sys.stdout.write('      {id}: [{date}] {value} interest\r\n'
                                     .format(id=loan_transaction['id'], date=loan_transaction['date'], value=loan_transaction['value']))
                    sys.stdout.flush()

            loan_fee = dict()
            loan_fee['id'] = loan_id
            loan_fee['date'] = transaction_date
            loan_fee['value'] = float(back_payment_table_rows[i].find_elements_by_tag_name("td")[2].text
                                                                .replace('€', '').replace(',', '.').strip())
            loan_fee['type'] = 'Gebühren'
            if loan_fee['value'] > 0:
                loan_transactions.append(loan_fee)
                if self.args and self.args.verbose and self.args.verbose >= 2:
                    sys.stdout.write('      {id}: [{date}] {value} fee\r\n'
                                     .format(id=loan_fee['id'], date=loan_fee['date'], value=loan_fee['value']))
                    sys.stdout.flush()

        return loan_transactions
