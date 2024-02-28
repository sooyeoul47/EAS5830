from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
from web3.middleware import geth_poa_middleware #Necessary for POA chains
import json
import sys
from pathlib import Path

source_chain = 'avax'
destination_chain = 'bsc'
contract_info = "contract_info.json"
private_key = "0xbe83d012497ec952d06a6096de569d1382321789f4719b099bb5d8d0d40d9cd0"
account_address = '0xDEdA37C517eF097c10D6501A33de377F194660a5'

def connectTo(chain):
    if chain == 'avax':
        api_url = f"https://api.avax-test.network/ext/bc/C/rpc" #AVAX C-chain testnet

    if chain == 'bsc':
        api_url = f"https://data-seed-prebsc-1-s1.binance.org:8545/" #BSC testnet

    if chain in ['avax','bsc']:
        w3 = Web3(Web3.HTTPProvider(api_url))
        # inject the poa compatibility middleware to the innermost layer
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def getContractInfo(chain):
    """
        Load the contract_info file into a dictinary
        This function is used by the autograder and will likely be useful to you
    """
    p = Path(__file__).with_name(contract_info)
    try:
        with p.open('r')  as f:
            contracts = json.load(f)
    except Exception as e:
        print( "Failed to read contract info" )
        print( "Please contact your instructor" )
        print( e )
        sys.exit(1)

    return contracts["source" if chain == source_chain else "destination"]

def scanBlocks(chain):
    """
        chain - (string) should be either "source" or "destination"
        Scan the last 5 blocks of the source and destination chains
        Look for 'Deposit' events on the source chain and 'Unwrap' events on the destination chain
        When Deposit events are found on the source chain, call the 'wrap' function the destination chain
        When Unwrap events are found on the destination chain, call the 'withdraw' function on the source chain
    """

    if chain not in ['source','destination']:
        print( f"Invalid chain: {chain}" )
        return
    
    #YOUR CODE HERE
    w3 = connectTo(chain)
    contracts = getContractInfo(chain)
    if chain == source_chain:
        contract_address, abi = contracts["address"], contracts["abi"]
    if chain == destination_chain:
        contract_address, abi = contracts["address"], contracts["abi"]

    # contract_address, abi = getContractInfo(chain)
    contract = w3.eth.contract(address=contract_address, abi=abi)

    start_block = w3.eth.block_number - 5

    if chain == source_chain:  #Source
        event_filter = contract.events.Deposit.create_filter(fromBlock=start_block)
        for event in event_filter.get_all_entries():
            print(f"Deposit Event Detected: {event.args}")
            txn = contract.functions.wrap(event.args['underlying_token'], event.args['recipient'], event.args['amount']).build_transaction({
                'chainId': w3.eth.chain_id,
                'gas': 5000000,
                'gasPrice': w3.to_wei('10', 'gwei'),
                'nonce': w3.eth.get_transaction_count(account_address),
            })
            signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(f'Transaction hash for registering token {event.args['underlying_token']}: {tx_hash.hex()}')
    elif chain == destination_chain:  #Destination
        event_filter = contract.events.Unwrap.create_filter(fromBlock=start_block)
        for event in event_filter.get_all_entries():
            print(f"Unwrap Event Detected: {event.args}")
            txn = contract.functions.withdraw(event.args['token'], event.args['recipient'], event.args['amount']).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 5000000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': w3.eth.get_transaction_count(account_address),
            })
            signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(f'Transaction hash for registering token {event.args['token']}: {tx_hash.hex()}')
            
