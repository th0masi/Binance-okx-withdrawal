import time
import ccxt
import random

#----options----#
cex_number = 2                                 # 1 - использовать Binance, 2 - использовать OKX
amount = [0.001, 0.002]                        # [min, max] сумма, выбирается рандомно
delay = [10, 50]                               # задержка между транзакциями, в секундах
shuffle_wallets = "no"                         # yes - перемешать кошельки, no - не перемешивать
symbolWithdraw = "ETH"                         # символ токена для вывода
network = "Arbitrum one"                       # ID сети, можно узнать в таблице
proxy_server = "http://login:password@ip:port" #укажите свой прокси для OKx
#----options----#

class API:
    binance_apikey = "YOUR_APIKEY_BINANCE"
    binance_apisecret = "YOUR_APISECRET_BINANCE"
    okx_apikey = "YOUR_APIKEY_OKX"
    okx_apisecret = "YOUR_APISECRET_OKX"
    okx_passphrase = "YOUR_PASSPHRASE"

proxies = {
  "http": proxy_server,
  "https": proxy_server,
}

def binance_withdraw(address, amount_to_withdrawal, wallet_number):
    exchange = ccxt.binance({
        'apiKey': API.binance_apikey,
        'secret': API.binance_apisecret,
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot'
        }
    })

    try:
        exchange.withdraw(
            code=symbolWithdraw,
            amount=amount_to_withdrawal,
            address=address,
            tag=None,
            params={
                "network": network
            }
        )
        print(f'\n>>>[Binance] Вывел {amount_to_withdrawal} {symbolWithdraw} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)
    except Exception as error:
        print(f'\n>>>[Binance] Не удалось вывести {amount_to_withdrawal} {symbolWithdraw}: {error} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)


def okx_withdraw(address, amount_to_withdrawal, wallet_number):
    exchange = ccxt.okx({
        'apiKey': API.okx_apikey,
        'secret': API.okx_apisecret,
        'password': API.okx_passphrase,
        'enableRateLimit': True,
        'proxies': proxies,
    })

    try:
        chainName = symbolWithdraw + "-" + network
        fee = get_withdrawal_fee(symbolWithdraw, chainName)
        exchange.withdraw(symbolWithdraw, amount_to_withdrawal, address,
            params={
                "toAddress": address,
                "chainName": chainName,
                "dest": 4,
                "fee": fee,
                "pwd": '-',
                "amt": amount_to_withdrawal,
                "network": network
            }
        )

        print(f'\n>>>[OKx] Вывел {amount_to_withdrawal} {symbolWithdraw} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)
    except Exception as error:
        print(f'\n>>>[OKx] Не удалось вывести {amount_to_withdrawal} {symbolWithdraw}: {error} ', flush=True)
        print(f'    [{wallet_number}]{address}', flush=True)


def get_withdrawal_fee(symbolWithdraw, chainName):
    exchange = ccxt.okx({
        'apiKey': API.okx_apikey,
        'secret': API.okx_apisecret,
        'password': API.okx_passphrase,
        'enableRateLimit': True,
        'proxies': proxies,
    })
    currencies = exchange.fetch_currencies()
    for currency in currencies:
        if currency == symbolWithdraw:
            currency_info = currencies[currency]
            network_info = currency_info.get('networks', None)
            if network_info:
                for network in network_info:
                    network_data = network_info[network]
                    network_id = network_data['id']
                    if network_id == chainName:
                        withdrawal_fee = currency_info['networks'][network]['fee']
                        if withdrawal_fee == 0:
                            return 0
                        else:
                            return withdrawal_fee
    raise ValueError(f" не могу получить значение комиссии, проверьте значения symbolWithdraw и network")

def choose_cex(address, amount_to_withdrawal, wallet_number):
    if cex_number == 1:
        binance_withdraw(address, amount_to_withdrawal, wallet_number)
    elif cex_number == 2:
        okx_withdraw(address, amount_to_withdrawal, wallet_number)
    else:
        raise ValueError("Неверное значение CEX. Значение должно быть 1 или 2.")

def shuffle(wallets_list, shuffle_wallets):
    numbered_wallets = list(enumerate(wallets_list, start=1))
    if shuffle_wallets.lower() == "yes":
        random.shuffle(numbered_wallets)
    elif shuffle_wallets.lower() == "no":
        pass
    else:
        raise ValueError("Неверное значение переменной 'shuffle_wallets'. Ожидается 'yes' или 'no'.")
    return numbered_wallets

if __name__ == "__main__":
    with open("wallets.txt", "r") as f:
        wallets_list = [row.strip() for row in f]
        numbered_wallets = shuffle(wallets_list, shuffle_wallets)
        print(f'developed by th0masi [https://t.me/thor_lab]')
        print(f'Number of wallets: {len(wallets_list)}')
        if cex_number == 1:
            cex = 'Binance'
        else:
            cex = 'OKX'
        print(f"CEX: {cex}")
        print(f"Amount: {amount[0]} - {amount[1]} {symbolWithdraw}")
        print(f"Network: {network}")
        time.sleep(random.randint(2, 4))

        for wallet_number, address in numbered_wallets:
            amount_to_withdrawal = round(random.uniform(amount[0], amount[1]), 5)
            choose_cex(address, amount_to_withdrawal, wallet_number)
            time.sleep(random.randint(delay[0], delay[1]))



