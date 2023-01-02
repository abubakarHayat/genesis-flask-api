'''
Api to get list of balances
'''
from flask_restful import Resource, abort
from models.block import Blockbalance

class BalanceList(Resource):
    '''
    provide get api for getting list of all wallet addresses
    '''
    def get(self):
        '''
        returns all wallet addresses and their correspoding balances
        from genesis block
        '''
        genesis_doc = Blockbalance.objects.first()
        if genesis_doc is None:
            abort(404, status="Blockchain hasn't started yet")
        genesis_block = genesis_doc.to_mongo().to_dict()
        return { 'balances': genesis_block['balances'] }
