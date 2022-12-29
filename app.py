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

from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
api = Api(app)

connect('flask', host=os.getenv('MONGO_URI'))


api.add_resource(Blockscan, '/blockscan')
api.add_resource(BalanceList, '/getAllBalances')
api.add_resource(Balance, '/getBalance/<string:address>')
api.add_resource(MedianBalance, '/getMedian')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
