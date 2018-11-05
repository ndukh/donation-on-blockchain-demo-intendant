# TelegramSender and Intendant
###  Both modules has a demonstration purpose.

It uses the [donation-on-blockhain-api](https://github.com/AplusD/dontation-on-blockchain-api)

#### TelegramSender
Telegram-bot interface, which allows to send a virtual donation to a random demo fund and get its ID.

#### Intendant
It randomly generates transactions (spendings) from incoming donations, imitating the real spendings.
Logic: it checks the balances of demo charity funds and spends random amount of money while the balance is positive.

### Deployment
Both modules are almost set up for deploying on IBM Bluemix CF (Python buildpack). Before deployment it is essential to:
- amend the parameters of `config_example.ini`;
- rename `config_example.ini` to `config.ini`;
- rename app in `manifest.yml`;
- *probably* make some other changes in [`manifest.yml`](https://www.ibm.com/support/knowledgecenter/en/SSMKFH/com.ibm.apmaas.doc/install/bluemix_sample_yml.htm) to increase performance of the instance(s).
