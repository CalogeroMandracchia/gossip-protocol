import asyncio
import logging
import sys

from tcp.client import Client
from peers.utils import get_list_seeds, get_list_peers

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s > %(message)s',
    stream=sys.stderr
)

log = logging.getLogger('discovery')

def discovery_peers():
    #TODO solve the big problem of dying in 5 minutes
    seeds = get_list_seeds()
    peers = get_list_peers()
    list_people_ill_ask = set(seeds + peers)
    #TODO if you don't have enough peers, consider taking it from the known.txt
    loop = asyncio.get_event_loop()
    for peer in list_people_ill_ask:
        try:
            coro = loop.create_connection(lambda: Client(), peer, 3338)
            #TODO if failed remove from peers
            _, proto = loop.run_until_complete(coro)
        except ConnectionRefusedError as exc:
            #TODO better logs with name of error
            log.debug("{}: {}".format(peer, exc))
        except Exception as exc:
            log.debug("{}: {}".format(peer, exc))


async def infinite_discovery_peers():
    while True:
        await asyncio.sleep(300)
        discovery_peers()
