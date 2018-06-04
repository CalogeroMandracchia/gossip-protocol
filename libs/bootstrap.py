from os.path import isfile

from tcp.server import Server

#TODO fai logging separato

def get_seeds(log, seeds_file):
    log.debug("seeds file is {}".format(seeds_file))
    with open(seeds_file) as seeds:
        list_seeds = seeds.read()
    if list_seeds == None:
        err_message = "seed file {} is empty".format(seeds_file)
        log.debug(err_message)
        raise IOError(err_message)
    log.debug("seeds read: " + ''.join(list_seeds))
    return list_seeds

def create_peers(log, peers_namefile = "./peers/peers.txt"):
    if isfile(peers_namefile):
        log.debug("peers file '{}' found".format(peers_namefile))
    else:
        open(peers_namefile, "w+")
        log.debug("peers file '{}' created".format(peers_namefile))

def create_known(log, known_namefile = "./peers/peers.txt"):
    if isfile(known_namefile):
        log.debug("known file '{}' found".format(known_namefile))
    else: 
        open(known_namefile, "w+")
        log.debug("known file '{}' created".format(known_namefile))

def create_banned(log, banned_namefile = "./peers/banned.txt"):
    if isfile(banned_namefile):
        log.debug("banned file '{}' found".format(banned_namefile))
    else: 
        open(banned_namefile, "w+")
        log.debug("banned file '{}' created".format(banned_namefile))

def create_seeds(log, data, seeds_namefile = "./peers/seeds.txt"):
    #TODO ma li scrive sti seeds??
    with open(seeds_namefile, "w") as f:
        f.write(data.join("|"))
    log.debug("seeds file '{}' created".format(seeds_namefile))

def start_server(log, loop, queue, serverport):
    server_address = ('localhost', serverport)
    coro_server = loop.create_server(lambda: Server(queue), *server_address)
    server = loop.run_until_complete(coro_server)
    log.debug('Serving on {}:{}'.format(*server.sockets[0].getsockname()))
    return server
    #TODO intercetta porta in uso