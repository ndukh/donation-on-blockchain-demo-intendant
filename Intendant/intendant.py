#  encoding: utf-8
import configparser
import logging
import random
import time
from threading import Thread

from Intendant.static import MyLogger
from Intendant.static import get

config = configparser.ConfigParser()
config.read('config.ini', 'utf-8')

SERVER = config.get('settings', 'SERVER')
ADD_TRANSACTION = config.get('settings', 'ADD_TRANSACTION')
GET_DONATIONS = config.get('settings', 'GET_DONATIONS')
LOGGING_SERVER = config.get('logging', 'SERVER')
LOGGING_PORT = config.get('logging', 'PORT')
TIMEOUT = config.get('settings', 'TIMEOUT')

ACCOUNTS = config.get('samples', 'ACCOUNTS').split(',')
FOUNDATIONS = config.get('samples', 'FOUNDATIONS').split(',')


class Intendant(Thread):
    def __init__(self, account):
        super().__init__()
        self.account = account
        self.balance = 0
        self.timeout = TIMEOUT
        self.donations = {}

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = MyLogger(LOGGING_SERVER, LOGGING_PORT)

    def run(self):
        while True:
            try:
                self.balance = self.check_balance()
                if self.balance > 0:
                    self.spend()
                time.sleep(int(self.timeout))
            except Exception as e:
                self.logger.error(e)

    def check_balance(self):
        result = get(SERVER + '/' + GET_DONATIONS, {'accountNumber': self.account})

        self.donations = {dct['donationId']: dct['balance'] for dct in result['output']}
        return sum(list(self.donations.values()))

    def spend(self):
        for donation_id, balance in self.donations.items():
            account = random.choice(ACCOUNTS)
            if balance > 100:
                amount = random.randint(2 * balance // 3, balance)
            else:
                amount = balance
            assert amount > 0
            params = {
                'donateId': donation_id,
                'amount': amount,
                'accountNumber': account,
                'purpose': '_'
            }
            answer = get(SERVER + '/' + ADD_TRANSACTION, params)
            self.logger.info(f'add_transaction answer = {answer}, params = {params}')
        return answer['result']


def main():
    for account_number in FOUNDATIONS:
        # individual thread for each fund
        intendant = Intendant(account_number)
        intendant.start()


if __name__ == "__main__":
    main()
