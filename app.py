'''
Api server
'''
import os
from flask import Flask
from flask_restful import Api

from apis.blockscan import Blockscan
from apis.median import MedianBalance
from apis.balance import Balance
from apis.balance_list import BalanceList
from apis.add_block import BlockAdd
from apis.blocks import Blocks
from apis.longest_chain import LongestChain
from flask_cors import CORS

from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
api = Api(app)
app.config['CORS_HEADERS'] = 'Content-Type'

connect('flask', host=os.getenv('MONGO_URI'))
api.add_resource(Blockscan, '/blockscan')
api.add_resource(BlockAdd, '/addBlock')
api.add_resource(Blocks, '/getAllChains')
api.add_resource(BalanceList, '/getAllBalances')
api.add_resource(Balance, '/getBalance/<string:address>')
api.add_resource(MedianBalance, '/getMedian')
api.add_resource(LongestChain, '/getLongestChain')

if __name__ == '__main__':
    app.run(port=5000)
