import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
cg = CoinGeckoAPI()

st.write("""
# Hindsight.Finance
""")
st.write("""
Crypto Token ROI analyzer 
""")
st.markdown("![Alt Text](https://media.giphy.com/media/YgkpHuZsVZlk8v9iCB/giphy.gif)")
st.write("""
Calculates the Return on Investment on a given token based on the amount invested and the time duration. Please Fomo responsibly.
""")
st.write('---')
#token list
token_name= ['ethereum','bitcoin','tether', 'binancecoin', 'cardano', 'ripple', 'dogecoin', 
'usd-coin', 'polkadot', 'uniswap', 'binance-usd', 'bitcoin-cash', 'litecoin', 'solana', 'chainlink', 
'matic-network', 'ethereum-classic', 'wrapped-bitcoin', 'internet-computer', 'theta-token', 'stellar', 
'vechain', 'dai', 'filecoin', 'tron', 'shiba-inu', 'aave', 'monero', 'eos', 'cosmos', 'compound-usd-coin', 
'crypto-com-chain', 'cdai', 'celsius-degree-token', 'pancakeswap-token', 'algorand', 'okb', 'compound-ether',
'compound-governance-token', 'maker', 'bitcoin-cash-sv', 'amp-token', 'terra-luna', 'neo', 'leo-token', 'klay-token',
'tezos', 'iota', 'ftx-token', 'avalanche-2', 'the-graph', 'thorchain', 'terrausd', 'havven', 'kusama', 'theta-fuel', 
'decred', 'bittorrent-2', 'huobi-token', 'safemoon', 'elrond-erd-2', 'sushi', 'hedera-hashgraph', 'waves', 'true-usd',
'staked-ether', 'dash', 'huobi-btc', 'yearn-finance', 'telcoin', 'zcash', 'chiliz', 'xdce-crowd-sale', 'nem', 'helium', 
'enjincoin', 'holotoken', 'quant-network', 'zilliqa', 'near', 'paxos-standard', 'blockstack', 'basic-attention-token', 
'kucoin-shares', 'nexo', 'mdex', 'ecomi', 'bitcoin-gold','decentraland', 'bancor', 
'liquity-usd', 'titanswap', 'xsushi', 'qtum', 'zencash', 'harmony', 'curve-dao-token', 'siacoin', 'digibyte', 'uma']
# select token
st.write('''## Select Cryptocurrency''')
selected_crypto_currency = st.selectbox('Select Crypto Currency', token_name )
st.write('You have selected',selected_crypto_currency)
id=selected_crypto_currency

# - Date of investment
st.write('''## Choose Date''')
today = datetime.utcnow().date()
previous_day = today - timedelta(days=1)
selected_historical_date = st.date_input("Date: ", value=previous_day, min_value=datetime(2015,1,1), max_value=previous_day)
st.write('You have selected',selected_historical_date)

# Select Base currency
st.write('''## Select Base Currency''')
selected_currency_type = st.selectbox('Select Currency', ['usd'])

# Amount invested
st.write('''## Specify Amount (in dollars $)''')
selected_amount = st.number_input(" Amount: ", min_value=1, max_value=999999999, value=1000)

#Loading Data
crypto_current = cg.get_price(id, vs_currencies=selected_currency_type)[id][selected_currency_type]

#Reformat Historical Date for next function
selected_historical_date_reformat = selected_historical_date.strftime("%d-%m-%Y")
selected_historical_date_datetime = datetime.strptime(selected_historical_date_reformat,"%d-%m-%Y")
selected_crypto_currency_historic = cg.get_coin_history_by_id(id, vs_currencies=selected_currency_type, date=selected_historical_date_reformat)['market_data']['current_price'][selected_currency_type]
selected_crypto_currency_historic = round(selected_crypto_currency_historic, 15)

st.write('---')
# Displaying Results 
st.write('''# Results''')
st.write('''## Historic Analysis''')

if selected_crypto_currency_historic == 0:
    st.write("You would have bought: 0",selected_crypto_currency)
else:
    st.write("You would have bought: ", round((selected_amount/selected_crypto_currency_historic),5),selected_crypto_currency)

st.write("At a price of $", selected_crypto_currency_historic,' per',selected_crypto_currency)

# Display Results 
st.write('''## Current Value''')
if selected_crypto_currency_historic == 0:
    total_coins = 0
else:
    total_coins = selected_amount/selected_crypto_currency_historic

current_selected_currency_type = total_coins * crypto_current
perc_change = (current_selected_currency_type - selected_amount)/(selected_amount)*100
selected_currency_type_diff = current_selected_currency_type - selected_amount

st.write("That is currently worth: $", round(current_selected_currency_type,2))
st.write("Which is a percentage change of ", round(perc_change, 2), "%")

st.write('---')
if selected_currency_type_diff == 0:
   st.write('''# You Broke Even''')
elif selected_currency_type_diff <= 0:
   st.write('''# You Would Have Lost''')
else:
   st.write('''# You Missed Out On''') 
st.write('$', abs(round(selected_currency_type_diff,2)),"!!!")

now = datetime.now()
historical_prices = cg.get_coin_market_chart_range_by_id(id, vs_currency=selected_currency_type, from_timestamp=selected_historical_date_datetime.timestamp(), to_timestamp=now.timestamp())['prices']

dates = []
prices = []

for x,y in historical_prices:
  dates.append(x)
  prices.append(y)

dictionary = {"Prices":prices, "Dates":dates}
df = pd.DataFrame(dictionary)
df['Dates'] = pd.to_datetime(df['Dates'],unit='ms',origin='unix')

st.line_chart(df.rename(columns={"Dates":"index"}).set_index("index"))

