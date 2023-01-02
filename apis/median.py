'''
Api to get median of all balances
'''
from flask_restful import Resource, abort
from models.block import Blockbalance
from utils.utility import calc_median

class MedianBalance(Resource):
    '''
    provides get api for calculating median balance
    '''
    def get(self):
        '''
        returns calculated media balance(s) and its wallet address
        '''
        genesis_doc = Blockbalance.objects.first()
        if genesis_doc is None:
            abort(404, status="Blockchain hasn't started yet")
        genesis_block = genesis_doc.to_mongo().to_dict()
        median = calc_median(genesis_block)
        return { "median": median }


