'''
Api to scan the block
'''
from flask_restful import Resource, reqparse
from models.block import Block
from utils.utility import update_balances

blockscan_args = reqparse.RequestParser()
blockscan_args.add_argument("hash", type=str, help='hash is required', required=True)
blockscan_args.add_argument("number", type=int, help='number is required', required=True)
blockscan_args.add_argument("prevhash", type=int, help='prevHash is required', required=True)
blockscan_args.add_argument("transfers", type=list, location='json')

class Blockscan(Resource):
    '''
    provides api for 'post' request on blockscan
    '''
    def post(self):
        '''
        Scans and updates Genesis block based on block received
        '''
        args = blockscan_args.parse_args()
        genesis_doc = Block.objects.first()
        genesis_block = genesis_doc.to_mongo().to_dict()
        updated_balances = update_balances(genesis_block['balances'], args)
        genesis_doc.update(balances=updated_balances)
        genesis_doc.save()

        return { "status": "Success" }
