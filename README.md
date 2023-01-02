## Backend Apis made in Python Flask (flask-restful)
---
1. #### Installation
- Install pip for python3
`sudo apt install python3-pip`
- Install python.
`sudo apt-get install python3.10`
- Check and make sure you have python version > 3
`python3 --version`

- Install virtualenv to create a virtual environemnt.
`sudo apt-get install virtualenv`

2. #### Setting up a virtual environment
- Create a directory for your project and navigate inside it.
`mkdir 'flask-backend'`
`cd 'flask-backend'`
- Create a virtual environment named 'venv' or any other name inside the directory.
`virtualenv venv`
- Activate the virtual environment.
`. venv/bin/activate`
or
`source venv/bin/activate`

3. #### Install required python packages
- Use the 'requirements.txt' to install the required packages.
`pip3 install -r requirements.txt'`
4. #### Start the server
- Start the flask server
`python3 app.py`

##### The server has started on 'localhost:5000'

---
### APIs
---
- ##### Following are the APIs provided! #####
1. **'/addBlock'** -> Adds a block to the chain.
2. **'/blockscan'** -> Scans the incoming block and updates the balances in genesis block.
3. **'/getAllChains'** -> Gets all the chains.
4. **'/getAllBalances'** -> Gets all the balances corresposning to the wallet addresses.
5. **'/getBalance/:walletAddress'** -> Gets corresponding balance.
6. **'/getMedian'** -> Gets Median of the balances.
7.  **'/getLongestChain'** -> Gets the longest chain.
