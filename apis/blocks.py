from flask_restful import Resource
from utils.utility import get_all_blocks

class Blocks(Resource):
    def get(self):
        return get_all_blocks()

