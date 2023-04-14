# Обновление
all-in-one withdrawal - https://github.com/th0masi/all-cex-withdrawal
Текущая версия не будет поддерживаться, создал новый со всеми биржами!

# Описание проекта

Cкрипт на Python для автоматического вывода токенов c бирж Binance или OKX.

# Настройки

```cex_number``` - указать номер биржи для вывода токенов (1 - Binance, 2 - OKX)  
```amount``` - указать минимальную и максимальную сумму для вывода токенов  
```delay``` - указать минимальную и максимальную задержку между транзакциями  
```shuffle_wallets``` - указать, нужно ли перемешивать кошельки перед выводом токенов (yes/no)  
```symbolWithdraw``` - символ токена для вывода  
```network``` - сеть для вывода  


```binance_apikey``` - API ключ для Binance  
```binance_apisecret``` - API секрет для Binance  
```okx_apikey``` - API ключ для OKX  
```okx_apisecret``` - API секрет для OKX  
```okx_passphrase``` - пароль для OKX  

# Использование

Сохранить файл с именем main.py  
Создать файл wallets.txt в корневой директории проекта с адресами кошельков, на которые будут выводиться токены    
Установить библиотеку ccxt   ```pip install ccxt```  
Открыть терминал и выполнить команду python main.py  

# Поддержка/Вопросы

Metamask: ```0x86B0ebc4F5dd71AD5ad37255681F6dc70e79D0F6```  
TG: @thorlab_chat
