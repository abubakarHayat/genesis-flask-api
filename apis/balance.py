'''
Api to get single balance
'''
from flask_restful import Resource, abort
from models.block import Blockbalance
from utils.utility import is_invalid_address

class Balance(Resource):
    '''
    provides post api for getting balance of specific
    wallet address
    '''
    def get(self, address):
        '''
        gets wallet address
        returns balance of corresponding wallet address
        '''
        genesis_doc = Blockbalance.objects.first()
        if genesis_doc is None:
            abort(404, status="Blockchain hasn't started yet")
        genesis_block = genesis_doc.to_mongo().to_dict()
        if is_invalid_address(genesis_block['balances'].keys(), address):
            abort(422, message='wallet address is invalid')
        balance  = genesis_block['balances'][address]
        return { address: balance }
