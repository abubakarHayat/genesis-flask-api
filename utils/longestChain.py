'''
longest chain
'''
from flask_restful import abort
from .utility import get_all_blocks
from .Middleware import Middleware

def get_longest_chain():
    '''
    Gets longest chain
    '''
    chain_data = get_all_blocks()
    if len(chain_data) == 0:
        abort(404, status="Blockchain hasn't started yet")
    elif len(chain_data) == 1:
        return chain_data

    # set Initial balance
    initialbalances = chain_data[0]['balances']

    # Create an instance of the Middleware class
    middleware = Middleware(initialbalances, 0)

    # Process each block in the chain data
    # when a new block is received then process that block through this function
    for block in chain_data:
        middleware.process_block(block)

    middleware.account_balances

    LongestChain = middleware.getLongestChain()
    return LongestChain
