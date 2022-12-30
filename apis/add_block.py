from flask_restful import Resource, abort
from mongoengine.queryset import QuerySet
from models.block import Block
from utils.longestChain import get_longest_chain
from utils.utility import update_balances

import os
import json

class BlockAdd(Resource):
    def get(self):
        try:
            BLOCK_FILE_PATH = os.path.abspath('./block_store/blocks.json')
            with open(BLOCK_FILE_PATH) as f:
                blocks = json.loads(f.read())

            block = Block.switch_collection(Block(),'addblock')
            new_block = QuerySet(Block ,block._get_collection())
            INDEX = new_block.all().count()

            block_to_add = blocks[INDEX]

            if INDEX == 0:
                blk = Block(
                    hash= block_to_add["hash"],
                    number= block_to_add["number"],
                    prevhash= block_to_add["prevhash"],
                    balances=block_to_add["balances"]
                )
            else:
                blk = Block(
                    hash= block_to_add["hash"],
                    transfers= block_to_add["transfers"],
                    number= block_to_add["number"],
                    prevhash= block_to_add["prevhash"],
                )
            blk.switch_collection('addblock')

            blk.save()
            if block_to_add["number"] == 0:
                # add genesis block to 'block' collection
                gen_block = Block(
                                hash= block_to_add["hash"],
                                number= block_to_add["number"],
                                prevhash= block_to_add["prevhash"],
                                balances=block_to_add["balances"]
                            )
                gen_block.save()
            elif block_to_add["number"] > 6:
                longest_chain = get_longest_chain()
                balance_block = longest_chain[block_to_add["number"] - 6]
                genesis_doc = Block.objects.first()
                genesis_block = genesis_doc.to_mongo().to_dict()
                updated_balances = update_balances(genesis_block['balances'], balance_block)
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
