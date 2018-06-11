import asyncio
from gossip import Gossip



def cb_process_data(data):
    print("processing dummy.. {}".format(data))

def cb_send_data():
    pass
    
my_gossip = Gossip("seeds.txt", cb_process_data, cb_send_data)
my_gossip.start()