import datetime
from iqoptionapi.stable_api import IQ_Option


# ::::: BALANCE FUNCTIONS :::::
def bal_inquiry(invest_percentage, invest_percentage_increment):
    balance = API.get_balance()
    if balance >= 20:
        return (balance * invest_percentage) / 100  # 5 % of balance
    elif 1 <= balance < 20:
        while True:
            net_invest = (balance * (invest_percentage + invest_percentage_increment)) / 100
            if net_invest >= 1:
                return net_invest
            else:
                invest_percentage_increment = min(invest_percentage_increment * 2, 95)
    else:
        raise ValueError('Balance in the account is less than 1\n')


# ::::: ORDER EXECUTIONS :::::
def order_exec(direction):
    money = bal_inquiry(investment_per, investment_per_increment)
    sts, prod_id = API.buy_digital_spot(pair, money, direction, expirations_time)
    if not sts:
        sts, prod_id = API.buy(money, pair, direction, expirations_time)
    trans_id.add(f"{direction}:{prod_id}")


API = IQ_Option("xyz.com", "xyz", "PRACTICE")
check, reason = API.connect()
print(check, reason, '\n')

# ::::: TRADE SYMBOL AND SETTINGS :::::
pair = 'EURUSD'
candle_size = 900  # In Seconds
expirations_time = 5  # In Minutes
num_records = 6

# ::::: PENDING ORDER STORAGE :::::
buy_side = set()
sell_side = set()
trans_id = set()

# ::::: BALANCE & INVESTMENT AMOUNT :::::
investment_per = 5  # 5 % of the balance will be invested in any order placed
investment_per_increment = 0.5  # % of mount increased if 5% of balance is  < 1
API.start_candles_stream(pair, candle_size, num_records)

while True:
    values = API.get_realtime_candles(pair, candle_size)
    opn, high, low, close, dt = [], [], [], [], []

    for timestamp in values:
        opn.append(values[timestamp]['open'])
        high.append(values[timestamp]['max'])
        low.append(values[timestamp]['min'])
        close.append(values[timestamp]['close'])
        dt.append(values[timestamp]['from'])

    current_close = close[-1]

    # ::::: BUY :::::
    if current_close in buy_side:
        buy_side.discard(current_close)
        order_exec('call')

    # ::::: SELL :::::
    if current_close in sell_side:
        sell_side.discard(current_close)
        order_exec('put')

    buy_side = set(filter(lambda x: x < current_close, buy_side))
    sell_side = set(filter(lambda x: x > current_close, sell_side))

    # ::::: CONDITIONS :::::
    # B >>>
    if (opn[0] >= close[0] and opn[1] < close[1] and opn[2] < close[2] and opn[3] < close[3] and opn[4] < close[4] and
        high[3] not in buy_side and datetime.datetime.now().timestamp() >= dt[5]) and close[4] > high[3]:
        buy_side.add(high[3])

    elif (opn[0] >= close[0] and opn[1] < close[1] and opn[2] < close[2] and opn[3] < close[3] and opn[4] < close[4] and
          high[3] not in buy_side and datetime.datetime.now().timestamp() >= dt[5]) and close[4] <= high[3]:
        sell_side.add(high[3])

    # S >>>
    elif (opn[0] <= close[0] and opn[1] > close[1] and opn[2] > close[2] and opn[3] > close[3] and opn[4] > close[4] and
          low[3] not in sell_side and datetime.datetime.now().timestamp() >= dt[5]) and close[4] >= low[3]:
        buy_side.add(low[3])

    elif (opn[0] <= close[0] and opn[1] > close[1] and opn[2] > close[2] and opn[3] > close[3] and opn[4] > close[4] and
          low[3] not in sell_side and datetime.datetime.now().timestamp() >= dt[5]) and close[4] < low[3]:
        sell_side.add(low[3])

    print(f':::::::::::::::::::::: {datetime.datetime.fromtimestamp(dt[-1])}')
    print(f'Buy Side: {buy_side}')
    print(f'Sell Side: {sell_side}')
    # print('Tans ID: {trans_id}')
