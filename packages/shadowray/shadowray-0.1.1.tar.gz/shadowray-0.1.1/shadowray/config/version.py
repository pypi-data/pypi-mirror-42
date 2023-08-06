VERSION_ID = "0.1.1"
AUTHOR = "RMT"
EMAIL = "d.rong@outlook.com"

COMMAND_LONG = ["version", "help", "subscribe-add=", "subscribe-update", "config-v2ray=", "config-subscribe=",
                "config-servers=", "autoconfig", "subscribe-update", "list", "start="]
COMMAND_SHORT = "vhs"

HELP_INFO = \
''' --help[-h]                      print help message
    --version[-v]                   show current version of shadowray
    --subscribe-add 'name:url'      add subscribe
    --subscribe-update              update subscribe
    --config-v2ray path             setup the path of v2ray binary
    --config-subscribe path         setup the path of subscribe file
    --config-servers path           setup the path of servers file
    --autoconfig                    setup basic setting automatic
    --subscribe-update              update subscribe
    --list                          show all servers
    --start[-s] index               start v2ray'''
