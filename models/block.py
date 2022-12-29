'''
Schema module for MongoDB Block document
'''
from mongoengine import Document, DictField, IntField

class Block(Document):
    '''
    Block Schema structure
    '''
    balances = DictField()
    hash = IntField(required=True, unique=True)
    prevhash = IntField(required=True, unique=True)
    number = IntField(required=True)
