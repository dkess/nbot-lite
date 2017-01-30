class ChannelJoin:
    def __init__(self, ircsend, config):
        self.ircsend = ircsend
        self.config_channels = set(config["channels"].split(","))
        self.autorejoin = config["channels"] != "0"
        self.botnick = config["nick"]

        self.kicked_from = set()

    def ircget(self, msg):
        try:
            if msg.split(" ")[1] == "001":
                self.ircsend("JOIN "+ (",".join(self.config_channels)))
        except IndexError:
            pass

