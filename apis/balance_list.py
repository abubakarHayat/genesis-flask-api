'''
Api to get list of balances
'''
from flask_restful import Resource
from models.block import Block

class BalanceList(Resource):
    '''
    provide get api for getting list of all wallet addresses
    '''
    def get(self):
        '''
        returns all wallet addresses and their correspoding balances
        from genesis block
        '''
        genesis_doc = Block.objects.first()
        genesis_block = genesis_doc.to_mongo().to_dict()
        return { 'balances': genesis_block['balances'] }
