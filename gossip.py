import asyncio
import logging
import sys
import queue

from libs.bootstrap import get_seeds, create_peers, create_known, create_banned, create_seeds, start_server
from libs.discovery import discovery_peers, infinite_discovery_peers
from libs.broadcast import broadcast


logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s > %(message)s',
    stream=sys.stderr
)

class Gossip:
    def __init__(self, seeds_file, cb_process_data, cb_send_data):
        self.log = logging.getLogger('Gossip')
        self.loop = asyncio.get_event_loop()
        self.incoming_queue = queue.Queue()
        self.outgoing_queue = queue.Queue()

        #TODO: take it from a config.gossip
        self.server_port = 3338
        self.peers_namefile = "peers.txt" 
        self.known_namefile = "known.txt"
        self.seeds_file = seeds_file

        self.log.debug("step #1: reading seeds file")
        self.list_seeds = get_seeds(self.log, self.seeds_file)

        self.log.debug("step #2: create seeds, peers, known files and banned if they do not exists")
        create_seeds(self.log, self.list_seeds)
        create_peers(self.log)
        create_known(self.log)
        create_banned(self.log)

        self.log.debug("step #3: start server listening on port {}".format(self.server_port))
        self.server = start_server(self.log, self.loop, self.incoming_queue, self.server_port)

        self.log.debug("step #4: launch network discovery")
        asyncio.ensure_future(discovery_peers())
        asyncio.ensure_future(infinite_discovery_peers())

        asyncio.ensure_future(self._process_incoming_data(cb_process_data))
        asyncio.ensure_future(self.send_data(cb_send_data))
        asyncio.ensure_future(broadcast(self.outgoing_queue))

    async def _process_incoming_data(self, cb):
        while True:
            try:
                await asyncio.sleep(1)
                data = self.incoming_queue.get(block=False)
                self.incoming_queue.task_done()
                data = data.decode()
                filtered_data = cb(data.decode())
                if filtered_data != None:
                    print('Message arrived: {}'.format(filtered_data))
                    self.outgoing_queue.put(data, block=False)
            except queue.Empty as exc:
                pass

    async def send_data(self, cb):
        while True:
            try:
                await asyncio.sleep(1)
                data = cb()
                if data != None:
                    self.outgoing_queue.put(data, block=False)
            except Exception as exc:
                print(exc)

    def start(self):
        self.loop.run_forever()