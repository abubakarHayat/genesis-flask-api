'''
Schema module for MongoDB Block document
'''
from mongoengine import Document, DictField, IntField, ListField

class Blockbalance(Document):
    '''
    Block Schema structure
    '''
    balances = DictField()
    hash = IntField(required=True, unique=True)
    prevhash = IntField(required=True)
    number = IntField(required=True)
    transfers = ListField()
