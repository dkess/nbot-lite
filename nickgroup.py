import itertools
import re
import os

class NickGroup:
    def __init__(self, ircsend, config):
        self.ircsend = ircsend
        self.all_nicks = {}

        try:
            self.prefix = config["nicklist prefix"]
        except KeyError:
            self.prefix = "!"

        # a list of channels that have not ended their list of NAMES
        self.names_printing = set()

    def nickgroup_intersect(self, nicks, groupname):
        nicks = nicks[:]
        o = set()
        try:
            with open(os.path.join(os.path.dirname(__file__), "resources", "factoids.txt")) as f:
                for l in f:
                    for n in nicks:
                        if (n not in o) and re.match(l[:-1], n, flags=re.IGNORECASE):
                            o.add(n)
        except IOError:
            pass
        return o

    def ircget(self, msg):
        smsg = msg.split(" ")
        try:
            if smsg[1] == "PRIVMSG":
                stxt = smsg[3][1:].partition(self.prefix)
                if not stxt[0]:
                    sender = smsg[0].split("!",1)[0]
                    chan = smsg[2].lower()
                    groupname = stxt[2]

                    response = self.nickgroup_intersect(self.all_nicks[chan], groupname)

                    self.ircsend("NOTICE {} :{}".format(sender, ", ".join(response)))

            if "!printnicks" in msg:
                print(self.all_nicks)

            # 353 means this is a list of NAMES
            if smsg[1] == "353":
                names_to_add = [n.lstrip("+~@&%") for n in itertools.chain([smsg[5][1:]], smsg[6:])]
                chan = smsg[4].lower()
                if chan in self.names_printing:
                    self.all_nicks[chan].append(names_to_add)
                else:
                    self.all_nicks[chan] = names_to_add
                    self.names_printing.add(chan)

            # 366 means the list of NAMES is over
            if smsg[1] == "366":
                chan = smsg[3].lower()
                try:
                    self.names_printing.remove(chan)
                except KeyError:
                    pass

            if smsg[1] == "JOIN":
                chan = smsg[2][1:].lower()
                try:
                    self.all_nicks[chan].append(smsg[0].split("!")[0])
                except KeyError:
                    pass

            if smsg[1] == "PART":
                chan = smsg[2].lower()
                try:
                    self.all_nicks[chan].remove(smsg[0].split("!")[0])
                except (KeyError, ValueError) as e:
                    pass

            if smsg[1] == "QUIT":
                nick = smsg[0].split("!")[0]
                for c in self.all_nicks.values():
                    try:
                        c.remove(nick)
                    except ValueError:
                        pass

            if smsg[1] == "KICK":
                chan = smsg[2].lower()
                nick = smsg[3]
                try:
                    self.all_nicks[chan].remove(nick)
                except (KeyError, ValueError) as e:
                    pass

            if smsg[1] == "NICK":
                oldnick = smsg[0].split("!")[0]
                newnick = smsg[2][1:]

                for c in self.all_nicks.values():
                    try:
                        c.remove(oldnick)
                        c.append(newnick)
                    except ValueError:
                        pass

        except IndexError:
            pass

