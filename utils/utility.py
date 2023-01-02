'''
Utility functions
'''
import math
import json
from mongoengine.queryset import QuerySet
from models.block import Blockbalance


def calc_median(genesis_block):
    '''
    calculates and returns median of balances
    '''
    balances = list(genesis_block['balances'].items())
    balances = sorted(balances, key=lambda item: item[1])
    balances_len = len(balances)
    mid = math.floor(balances_len/2)

    if balances_len % 2 != 0:
        return balances[mid][1]

    return int((balances[mid][1] + balances[mid][1])/2)

def update_balances(balances, args):
    '''
    Updates 'balances' according to provides 'args'
    '''
    for transaction in args['transfers']:
        sender = transaction['sender']
        receiver = transaction['receiver']
        amount = transaction['amount']

        sender_amt = balances[sender]
        balances[sender] = sender_amt - amount

        receiver_amt = balances[receiver]
        balances[receiver] = receiver_amt + amount
    return balances

def is_invalid_address(keys, address):
    '''
    Checks if a wallet address is invalid
    '''
    if address not in keys:
        return True
    return False

def get_all_blocks():
    '''
    Gets all blocks from 'blocklists' collection
    '''
    block = Blockbalance.switch_collection(Blockbalance(),'blocklists')
    new_block = QuerySet(Blockbalance ,block._get_collection())
    blk = new_block.all().to_json()
    return json.loads(blk)

def get_block_to_add(block_to_add, INDEX):
    if INDEX == 0:
        return Blockbalance(
            hash= block_to_add["hash"],
            number= block_to_add["number"],
            prevhash= block_to_add["prevhash"],
            balances=block_to_add["balances"]
        )

    return Blockbalance(
        hash= block_to_add["hash"],
        transfers= block_to_add["transfers"],
        number= block_to_add["number"],
        prevhash= block_to_add["prevhash"],
    )
