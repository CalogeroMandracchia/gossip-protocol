def get_list_peers():
    with open("./peers/peers.txt") as file_peers:
        list_peers = file_peers.read()
        #TODO remove 127.0.0.1
    return list_peers.split("|")

def write_peers(peers):
    with open("./peers/peers.txt", 'w') as file_peers:
        list_peers = file_peers.write('|'.join(peers))

def get_list_seeds():
    with open("./peers/seeds.txt") as file_peers:
        list_peers = file_peers.read()
        #TODO remove 127.0.0.1
    return list_peers.split("|")

