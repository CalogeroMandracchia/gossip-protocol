import asyncio
import logging
import sys
import json

from protocol.outgoing import is_cmd_outgoing_protocol

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s > %(message)s',
    stream=sys.stderr
)

class Client(asyncio.Protocol):
    
    def __init__(self):
        self.log = logging.getLogger('client')
        self.address = None
        self.transport = None
    
    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log.debug('{}:{} connected'.format(*self.address))
    
    def data_received(self, data):
        try:
            data = json.loads(data.decode())
            self.log.debug('{}:{} just sent {!r}'.format(*self.address, data))
            #TODO is ip banned? -> self.connection_lost() "IP is banned"
            res = is_cmd_outgoing_protocol(data)
            if res == False:
                self.ban()
            if res == True:
                pass
            else:
                #TODO this point should never ne reached
                self.log.debug('{}:{} something went wrong: {}'.format(*self.address, res))
                self.transport.write(str.encode(res))
        except json.decoder.JSONDecodeError as exc:
            self.log.debug('{}:{} sent malformed data: {}'.format(*self.address, data))
            self.ban()
        except KeyError as exc:
            self.log.debug('{}:{} sent unrecognized keys: {}'.format(*self.address, data))
            self.ban()
        except TypeError as exc:
            self.log.debug('{}:{} did not send a key: {}'.format(*self.address, exc))
            self.ban()
        except Exception as exc:
            self.log.debug('{}:{} unexpected error! PLEASE report this on https://github.com/CalogeroMandracchia/gossip-protocol/issues : {}'.format(*self.address, exc))
 

    def eof_received(self):
        self.log.debug('{}:{} sent EOF'.format(*self.address))

    def connection_lost(self, error=""):
        self.log.debug('{}:{} disconnected'.format(*self.address))
        self.transport.close()

    def ban(self):
        #TODO implement
        #self.address[0]
        self.log.debug('{}:{} will be banned'.format(*self.address))
        self.transport.close()