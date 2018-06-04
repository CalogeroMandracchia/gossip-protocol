import asyncio
import logging
import sys

from tcp.client import Client
from peers.utils import get_list_peers

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s > %(message)s',
    stream=sys.stderr
)

log = logging.getLogger('broadcast')

def broadcast(cb):
    while True: 
        print("retrieving from cb")
        asyncio.sleep(10)
        data = cb()
        if data != None:
            log.debug("sending data: {}".format(data))
            send_data(data)
        asyncio.sleep(10)

def send_data(data):
    peers = get_list_peers()
    #TODO if you don't have enough peers, consider taking it from the known.txt
    loop = asyncio.get_event_loop()
    for peer in peers:
        try:
            coro = loop.create_connection(lambda: Client(), peer, 3338)
            #TODO if failed remove from peers
            _, protocol = loop.run_until_complete(coro)
            protocol.transport.write(data)
        except ConnectionRefusedError as exc:
            log.debug(exc)
        except Exception as exc:
            log.debug(exc)