import asyncio
import logging
import sys
import queue

from tcp.client import Client
from peers.utils import get_list_peers

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s > %(message)s',
    stream=sys.stderr
)

log = logging.getLogger('broadcast')


async def broadcast(q):
    while True:
        try:
            await asyncio.sleep(10)
            data = q.get(block=False)
            q.task_done()
            #TODO why data is already bytes?
            #data = str.encode(data)
            await send_data(data)
        except queue.Empty:
            log.debug("queue.Empty")


async def send_data(data):
    try:
        peers = get_list_peers()
        #TODO if you don't have enough peers, consider taking it from the known.txt
        for peer in peers:
            loop = asyncio.get_event_loop()
            log.debug("-{}- im sending data -{}-..".format(peer, data))
            coro = loop.create_connection(lambda: Client(), peer, 3338)
            _, protocol = await coro
            protocol.transport.write(data.encode(data))
            #protocol.transport.close()
    except ConnectionRefusedError as exc:
        #TODO better logs with name of error
        log.debug("{}: {}".format(peer, exc))
    except Exception as exc:
        log.debug("{}: {}".format(peer, exc))