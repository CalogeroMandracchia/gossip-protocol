import asyncio
import logging
import sys

from tcp.client import Client
from peers.utils import get_list_seeds, get_list_peers
from protocol.outgoing import getaddr

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s > %(message)s',
    stream=sys.stderr
)

log = logging.getLogger('discovery')

async def discovery_peers():
    try:
        log.debug("start discovering peers")
        #TODO solve the big problem of dying in 5 minutes
        seeds = get_list_seeds()
        peers = get_list_peers()
        to_be_filtered = set(seeds + peers)
        list_people_ill_ask = list(filter(None, to_be_filtered))
        #TODO if you don't have enough peers, consider taking it from the known.txt
        for peer in list_people_ill_ask:
            loop = asyncio.get_event_loop()
            log.debug("-{}- im going to try to connect now".format(peer))
            coro = loop.create_connection(lambda: Client(), peer, 3338)
            _, protocol = await coro
            #TODO ask addresses
            log.debug("i'm sending to -{}- this: -{}-".format(peer, getaddr()))
            protocol.transport.write(str.encode(getaddr()))
            protocol.transport.close()
    except ConnectionRefusedError as exc:
        #TODO better logs with name of error
        log.debug("{}: {}".format(peer, exc))
    except Exception as exc:
        log.debug("{}: {}".format(peer, exc))

async def infinite_discovery_peers():
    while True:
        try:
            await asyncio.sleep(10)
            await asyncio.wait_for(discovery_peers(), 10)
        except asyncio.TimeoutError as exc:
            log.debug(exc)