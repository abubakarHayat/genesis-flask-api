'''
Addition of block in blocklists collection
'''
import os
import json
from flask_restful import Resource, abort
from mongoengine.queryset import QuerySet
from models.block import Blockbalance
from utils.longestChain import get_longest_chain
from utils.utility import update_balances
from utils.utility import get_block_to_add

class BlockAdd(Resource):
    '''
    addBlock API
    '''
    def post(self):
        try:
            NUM_OF_PENDING_BLOCKS = 6
            BLOCK_FILE_PATH = os.path.abspath('./block_store/blocks.json')
            with open(BLOCK_FILE_PATH) as file:
                blocks = json.loads(file.read())

            block = Blockbalance.switch_collection(Blockbalance(),'blocklists')
            new_block = QuerySet(Blockbalance, block._get_collection())
            INDEX = new_block.all().count()
            block_to_add = blocks[INDEX]
            blk = get_block_to_add(block_to_add, INDEX)
            blk.switch_collection('blocklists')
            blk.save()

            if block_to_add["number"] == 0:
                # add genesis Blockbalance to 'Blockbalance' collection
                gen_block = Blockbalance(
                                hash= block_to_add["hash"],
                                number= block_to_add["number"],
                                prevhash= block_to_add["prevhash"],
                                balances=block_to_add["balances"]
                            )
                gen_block.save()
            elif block_to_add["number"] > 6:
                longest_chain = get_longest_chain()
                balance_block = longest_chain[block_to_add["number"] - NUM_OF_PENDING_BLOCKS]
                # get genesis block
                genesis_doc = Blockbalance.objects.first()
                # convert Blockbalance type object to python dict
                genesis_block = genesis_doc.to_mongo().to_dict()
                updated_balances = update_balances(genesis_block['balances'], balance_block)
                # update genesis block with updated balances, hash, prevhash & number
                genesis_doc.update(
                    balances=updated_balances,
                    hash=balance_block["hash"],
                    prevhash=balance_block["prevhash"],
                    number=balance_block["number"],
                    )
                genesis_doc.save()

            return { "status": "Success" }
        except:
            abort(500, message="An error occured")
