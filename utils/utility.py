'''
Utility functions
'''
import math
from models.block import Block
from mongoengine.queryset import QuerySet
import json

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
    if address not in keys:
        return True
    return False

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def get_all_blocks():
    block = Block.switch_collection(Block(),'addblock')
    new_block = QuerySet(Block ,block._get_collection())
    blk = new_block.all().to_json()
    return json.loads(blk)
