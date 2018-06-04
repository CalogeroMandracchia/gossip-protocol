import asyncio
from gossip import Gossip



def cb_process_data(data):
    print("processing dummy.. {}".format(data))

def cb_send_data():
    num = 1
    while True:
        asyncio.sleep(10)
        num = num + 1
        return str(num)
    
my_gossip = Gossip(cb_process_data, cb_send_data)
my_gossip.start()