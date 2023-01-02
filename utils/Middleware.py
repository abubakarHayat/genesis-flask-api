import copy


class Middleware:
    def __init__(self, balances, currentheight):
        self.account_balances = balances
        self.cachedBalance = balances

        self.currentHeight = currentheight
        self.currentCachedHeight = currentheight
        self.sideNodes = {}
        self.dicthashNode = {0: []}
        self.numberofBlocksProcessed = 0
        self.longestChainHash = None

    def process_block(self, block):
        '''Process a new block that has been added to the blockchain.
            Checks if with more than current height is added so add its new height
            else makes side chains
        '''
        # key -> (blockNumber, blockHash)
        # value -> block
        self.sideNodes[(block['number'], block['hash'])] = block

        # Check & add to other chains if same height or less than current height
        if (block['number'] <= self.currentHeight):
            self.dicthashNode[block['number']] += [block['hash']]
        # if greater than current height then make this longest chain & recompute balances
        elif (block['number'] > self.currentHeight):

            self.currentHeight = block['number']
            self.longestChainHash = block['hash']

            self.dicthashNode[block['number']] = [block['hash']]

            # Calculating balances for new longest chain
            temp = block['number']
            del self.account_balances
            self.account_balances = copy.copy(self.cachedBalance)

            prevhash = block['hash']
            for i in range(self.currentCachedHeight, block['number']+1):
                for transfer in self.sideNodes[(temp, prevhash)]['transfers']:
                    self.account_balances[transfer["sender"]
                                          ] -= transfer["amount"]
                    self.account_balances[transfer["receiver"]
                                          ] += transfer["amount"]

                # move to prev block in the longest chain
                self.sideNodes[(temp, prevhash)]['prevhash']
                prevhash = self.sideNodes[(temp, prevhash)]['prevhash']
                temp -= 1

            self.update_height(block)
        self.numberofBlocksProcessed += 1

    def cleanUpchain(self, cleanUpheight):
        for key, values in self.dicthashNode.items():
            if (key < cleanUpheight):
                for value in values:
                    del self.sideNodes[(key, value)]

        for i in range(cleanUpheight):
            del self.dicthashNode[i]

    def getLongestChain(self):

        temp = self.currentHeight
        prevhash = self.longestChainHash
        toReturn = []
        for i in range(self.currentCachedHeight,  self.currentHeight+1):
            toReturn.insert(0, self.sideNodes[(temp, prevhash)])
            # move cursor to previous chain node
            prevhash = self.sideNodes[(temp, prevhash)]['prevhash']
            temp -= 1

        return toReturn

    def update_height(self, block):
        '''Update the cached view with the current account balances.'''
        self.cached_view = sorted(self.account_balances.values())

    def print_side_chain(self):
        for key, value in self.sideNodes:
            print(f"{key}: {value}\n")

    def calculate_median(self):
        '''Calculate and return the median of the current account balances.'''
        if len(self.cached_view) % 2 == 0:
            # If there is an even number of account balances, return the average of the two middle values
            return (self.cached_view[len(self.cached_view) // 2 - 1] + self.cached_view[len(self.cached_view) // 2]) / 2
        else:
            # If there is an odd number of account balances, return the middle value
            return self.cached_view[len(self.cached_view) // 2]
