import json
from peers.utils import get_list_peers, write_peers

def addr():
    list_peers = get_list_peers()
    message = json.dumps({"cmd": "addr", "data": list_peers})
    return message

def verify_addr(new_peers):
    #TODO unify code in a lib, the -30: stuff
    list_peers = get_list_peers()
    eliminate_dup = set(list_peers + new_peers)
    truncate_peers = list(eliminate_dup)[-30:]
    write_peers(truncate_peers)
    return True

list_cmd = {
    "getaddr": addr,
    "addr": verify_addr
}

def is_cmd_incoming_protocol(cmd):
    res = list_cmd.get(cmd, None)
    if res == None:
        return None
    else:
        return res()