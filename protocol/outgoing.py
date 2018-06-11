import json
from peers.utils import get_list_peers, write_peers

def getaddr():
    print("preparing getaddr for asking")
    message = json.dumps({"cmd": "getaddr"})
    return message

def verify_addr(new_peers):
    #TODO verificate new_peers are real, otherwise... BAN IP!
    #TODO add new cmd for ping-pong, to check if someone is alive/still alive-
    list_peers = get_list_peers()
    eliminate_dup = set(list_peers + new_peers)
    truncate_peers = list(eliminate_dup)[-30:]
    write_peers(truncate_peers)
    return True

list_cmd = {
    "addr": verify_addr
}

def is_cmd_outgoing_protocol(data):
    if not "cmd" in data:
        return False

    cmd = list_cmd.get(data["cmd"], False)
    if not cmd:
        return False

    res = None
    if "data" in data:
        res = cmd(data["data"])
    else:
        res = cmd()
    return res