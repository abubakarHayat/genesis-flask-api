from flask_restful import Resource
from utils.longestChain import get_longest_chain

class LongestChain(Resource):
    def get(self):
      return get_longest_chain()
