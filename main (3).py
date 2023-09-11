import time
import requests
import hmac
import hashlib

bas = ('''
██████╗ ██╗   ██╗██████╗ ██╗████████╗     █████╗ ██████╗ ██╗    ███████╗ ██████╗ ███████╗████████╗
██╔══██╗╚██╗ ██╔╝██╔══██╗██║╚══██╔══╝    ██╔══██╗██╔══██╗██║    ██╔════╝██╔═══██╗██╔════╝╚══██╔══╝
██████╔╝ ╚████╔╝ ██████╔╝██║   ██║       ███████║██████╔╝██║    ███████╗██║   ██║█████╗     ██║   
██╔══██╗  ╚██╔╝  ██╔══██╗██║   ██║       ██╔══██║██╔═══╝ ██║    ╚════██║██║   ██║██╔══╝     ██║   
██████╔╝   ██║   ██████╔╝██║   ██║       ██║  ██║██║     ██║    ███████║╚██████╔╝██║        ██║   
╚═════╝    ╚═╝   ╚═════╝ ╚═╝   ╚═╝       ╚═╝  ╚═╝╚═╝     ╚═╝    ╚══════╝ ╚═════╝ ╚═╝        ╚═╝   
''')
spot = ('''
███████╗██████╗  ██████╗ ████████╗
██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
███████╗██████╔╝██║   ██║   ██║   
╚════██║██╔═══╝ ██║   ██║   ██║   
███████║██║     ╚██████╔╝   ██║   
╚══════╝╚═╝      ╚═════╝    ╚═╝   
''')
futures = ('''
███████╗██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗███████╗
██╔════╝██║   ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝██╔════╝
█████╗  ██║   ██║   ██║   ██║   ██║██████╔╝█████╗  ███████╗
██╔══╝  ██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝  ╚════██║
██║     ╚██████╔╝   ██║   ╚██████╔╝██║  ██║███████╗███████║
╚═╝      ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
''')
price_name = ('''
██████╗ ██████╗ ██╗ ██████╗███████╗
██╔══██╗██╔══██╗██║██╔════╝██╔════╝
██████╔╝██████╔╝██║██║     █████╗  
██╔═══╝ ██╔══██╗██║██║     ██╔══╝  
██║     ██║  ██║██║╚██████╗███████╗
╚═╝     ╚═╝  ╚═╝╚═╝ ╚═════╝╚══════╝
''')

secret_key = None
api_key = None

with open('api_keys.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    if line.startswith('api_key='):
        api_key = line.split('=')[1].strip()
    elif line.startswith('secret_key='):
        secret_key = line.split('=')[1].strip()  #Достается апи из тхт

# -----------------------------------------------------------------------------------------------------------------------------        
     
def hashing(query_string):   #какая то хуйня???
    return hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def futures_market_open_order(symbol, side, orderType, qty, category='linear'):      #Фьючерсы маркет открыть ордер
    url = 'https://api.bybit.com/v5/order/create'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "side": "{side}", "orderType": "{orderType}", "qty": "{qty}", "category": "{category}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)

    headers = {
     'X-BAPI-API-KEY': api_key,
     'X-BAPI-TIMESTAMP': str(current_time),
     'X-BAPI-SIGN': sign,
     'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)

# -----------------------------------------------------------------------------------------------------------------------------

def futures_limit_open_order(symbol, side, orderType, qty, price, category='linear'):      #Фьючерсы лимитка открыть ордер
    url = 'https://api.bybit.com/v5/order/create'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "side": "{side}", "orderType": "{orderType}", "price": "{price}", "qty": "{qty}", "category": "{category}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)

    headers = {
     'X-BAPI-API-KEY': api_key,
     'X-BAPI-TIMESTAMP': str(current_time),
     'X-BAPI-SIGN': sign,
     'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)
    
# -----------------------------------------------------------------------------------------------------------------------------  

def futures_cancel_order(symbol, category='linear'):      #Фьючерсы маркет закрыть ордер
    url = 'https://api.bybit.com/v5/order/cancel-all'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "category": "{category}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)    

    headers = {
     'X-BAPI-API-KEY': api_key,
     'X-BAPI-TIMESTAMP': str(current_time),
     'X-BAPI-SIGN': sign,
     'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)
# -----------------------------------------------------------------------------------------------------------------------------  

def futures_leverage_order(symbol, Leverage='1', category='linear'):      #Фьючерсы плечо
    url = 'https://api.bybit.com/v5/position/set-leverage'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "buyLeverage": "{Leverage}", "sellLeverage": "{Leverage}", "category": "{category}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)    

    headers = {
     'X-BAPI-API-KEY': api_key,
     'X-BAPI-TIMESTAMP': str(current_time),
     'X-BAPI-SIGN': sign,
     'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)
  
# -----------------------------------------------------------------------------------------------------------------------------  

def spot_market_open_order(symbol, side, orderType, qty, category='spot'):        #спот маркет купить/продать
    url = 'https://api.bybit.com/v5/order/create'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "side": "{side}", "orderType": "{orderType}", "qty": "{qty}", "category": "{category}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)

    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-TIMESTAMP': str(current_time),
        'X-BAPI-SIGN': sign,
        'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)  

# -----------------------------------------------------------------------------------------------------------------------------  

def spot_limit_open_order(symbol, side, orderType, qty, price, category='spot'):      #спот лимитка купить/продать
    url = 'https://api.bybit.com/v5/order/create'
    current_time = int(time.time() * 1000)
    data = '{' + f'"symbol": "{symbol}", "side": "{side}", "orderType": "{orderType}", "price": "{price}", "qty": "{qty}", "category": "{category}"' + '}'
    sign = hashing(str(current_time) + api_key + '5000' + data)

    headers = {
     'X-BAPI-API-KEY': api_key,
     'X-BAPI-TIMESTAMP': str(current_time),
     'X-BAPI-SIGN': sign,
     'X-BAPI-RECV-WINDOW': str(5000)
    }

    response = requests.post(url=url, headers=headers, data=data)
    print(response.text)

# -----------------------------------------------------------------------------------------------------------------------------  

def get_price(symbol):                      #узнать цену
    url = f'https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}USDT'
    response = requests.get(url=url)
    data = response.json()
    usd_index_price = data["result"]["list"][0]["usdIndexPrice"]
    print(f"Цена {symbol} = {usd_index_price}$")

# -----------------------------------------------------------------------------------------------------------------------------  

def get_price(symbol):
    url = f'https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}USDT'
    response = requests.get(url=url)
    data = response.json()
    usd_index_price = data["result"]["list"][0]["usdIndexPrice"]
    print(f"Цена {symbol} = {usd_index_price}$")

def start():
    print(bas)
    print(" 1. Спот\n 2. Фьючерсы\n 3. Узнать цены\n 4. Выйти\n")
    match input("Ваш выбор? "):
        case '1':
            print(spot)
            choose = input("\nКакой вариант торговли? \n 1. Рыночный \n 2. Лимитный \n 3. Назад \n")
            if choose == "1":                
                symbol = input("каким токеном торговать? ( например BTC, ETH, LTC и тд ) ").upper()
                get_price(symbol=f'{symbol}')
                side = 'Buy' if input(" 1. Купить\n 2. Продать\n ") == "1" else 'Sell'
                qty  = input("На какую сумму купить(USDT)/продать(TOKEN)? ")
                spot_market_open_order(symbol=f'{symbol}USDT', side=f'{side}', orderType='Market', qty=f"{qty}")
            elif choose == "2":
                symbol = input("каким токеном торговать? ( например BTC, ETH, LTC и тд ) ").upper()
                get_price(symbol=f'{symbol}')
                side = 'Buy' if input(" 1. Купить\n 2. Продать\n ") == "1" else 'Sell'
                price = float(input("Цена лимитной покупки/продажи: "))
                qty  = input("На какую сумму купить(USDT)/продать(TOKEN)? ")
                spot_limit_open_order(symbol=f'{symbol}USDT', side=f'{side}', orderType='Limit', qty=f'{qty}', price=f'{price}')             
            else:
                start()
        case '2':
            print(futures)
            choose = input("\nКакой вариант торговли? \n 1. Рыночный \n 2. Лимитный \n 3. Назад \n")
            if choose == "1":                
                symbol = input("каким токеном торговать? ( например BTC, ETH, LTC и тд ) ").upper()
                get_price(symbol=f'{symbol}')
                Leverage = input("Установите Плечо: ")
                futures_leverage_order(symbol=f'{symbol}USDT', Leverage=f'{Leverage}')
                side = 'Buy' if input(" 1. Лонг\n 2. Шорт\n ") == "1" else 'Sell'
                qty  = input("сумма входа: ")
                futures_market_open_order(symbol=f'{symbol}USDT', side=f'{side}', orderType='Market', qty=f"{qty}")
            elif choose == "2":
                symbol = input("1каким токеном торговать? ( например BTC, ETH, LTC и тд ) ").upper()
                get_price(symbol=f'{symbol}')
                Leverage = input("Установите Плечо: ")
                futures_leverage_order(symbol=f'{symbol}USDT', Leverage=f'{Leverage}')
                side = 'Buy' if input(" 1. Лонг\n 2. Шорт\n ") == "1" else 'Sell'
                price = float(input("Цена лимитной покупки/продажи: "))
                qty  = input("Сумма входа:  ")
                futures_limit_open_order(symbol=f'{symbol}USDT', side=f'{side}', orderType='Limit', qty=f'{qty}', price=f'{price}')
            else:
                start()
        case '3':
            print(price_name)
            while True:
                print("(Чтобы выйти введите 0)\n")
                symbol = input(" Введите токен: ").upper()
                if symbol == "0":
                    start()
                    return
                get_price(symbol=f'{symbol}')
        case "4":
            return
        case _:
            start()        


            


if __name__ == '__main__':
    start()


