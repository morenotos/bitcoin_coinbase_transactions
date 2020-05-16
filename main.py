import requests
import json
import pandas as pd
#from time import sleep


base_url = "https://blockstream.info/api"
#change the range to get to the block height.
block_height = [i for i in range(101)]

block_rewards = []
block_reward_addresses = []
block_coinbase_txid = []
coinbase_tx_df = pd.DataFrame(columns = [])



for block in block_height:
  block_hash_url = base_url + '/block-height/' + str(block)
  #print(block_hash_url)
  block_hash = requests.get(block_hash_url).text
  #print('The hash of block ' + str(block_height) + ' is ' + str(block_hash))


  #Coinbase transaction
  coinbase_txid_url = base_url + '/block/' + str(block_hash) + '/txid/0'
  coinbase_txid = requests.get(coinbase_txid_url).text
  block_coinbase_txid.append(coinbase_txid)
  #print(coinbase_txid)
  coinbase_tx_url = base_url + '/tx/' + str(coinbase_txid)
  coinbase_tx = requests.get(coinbase_tx_url).text
  parsed_coinbase_tx = json.loads(coinbase_tx)
  json_coinbase_tx = json.dumps(parsed_coinbase_tx, indent = 4)
  print(json_coinbase_tx)

  try:
    block_reward = parsed_coinbase_tx['vout'][0]['value']
    block_reward_address = parsed_coinbase_tx['vout'][0]['scriptpubkey_address']
    block_rewards.append(block_reward)
    block_reward_addresses.append(block_reward_address)
    print('Got block reward and block reward address for block ' + str(block))
  except KeyError:
    block_reward = parsed_coinbase_tx['vout'][0]['value']
    block_reward_address = parsed_coinbase_tx['vout'][0]['scriptpubkey']
    block_rewards.append(block_reward)
    block_reward_addresses.append(block_reward_address)
    print('Got block reward and block reward address for block ' + str(block))
    
#print(block_rewards)
#print(block_reward_addresses)
coinbase_tx_df['coinbase_tx_id'] = pd.Series(block_coinbase_txid).values
coinbase_tx_df['reward'] = pd.Series(block_rewards).values
coinbase_tx_df['address'] = pd.Series(block_reward_addresses).values

print(coinbase_tx_df.head())

coinbase_tx_df.to_csv('coinbase_tx_data.csv')
print('Coinbase tx data .csv file saved to folder')



