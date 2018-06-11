import asyncio
import logging
import sys
import json

from protocol.incoming import is_cmd_incoming_protocol

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s > %(message)s',
    stream=sys.stderr
)

class Server(asyncio.Protocol):
    def __init__(self, queue):
        self.log = logging.getLogger('server')
        self.address = None
        self.transport = None
        self.queue = queue

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log.debug('{}:{} connected'.format(*self.address))
        #TODO add in the known list

    def data_received(self, data):
        try:
            data = json.loads(data.decode())
            self.log.debug('{}:{} sent -{}-'.format(*self.address, data))
            #TODO is ip banned? -> self.connection_lost("IP is banned")
            res = is_cmd_incoming_protocol(data["cmd"])
            if res != None: # so it is a command 
                self.transport.write(str.encode(res))
            else: # it is not a command
                self.queue.put(data, block=False)
                self.log.debug('{}:{} just sent {!r}'.format(*self.address, data))

        except json.decoder.JSONDecodeError as exc:
            self.log.debug('{}:{} sent malformed data: {}'.format(*self.address, data))
        except Exception as exc:
            self.log.debug('{}:{} unexpected error! PLEASE report this on https://github.com/CalogeroMandracchia/gossip-protocol/issues : {}'.format(*self.address, exc))
        finally:
            self.connection_lost()

    def eof_received(self):
        self.log.debug('{}:{} sent EOF'.format(*self.address))

    def connection_lost(self, error=""):
        self.log.debug('{}:{} disconnected'.format(*self.address))
        self.transport.close()