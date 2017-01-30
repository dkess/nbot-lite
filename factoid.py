import os
import random

class Factoid:
    def __init__(self, ircsend, config):
        self.ircsend = ircsend

        try:
            self.prefix = config["factoid prefix"]
        except KeyError:
            self.prefix = "!"

    def get_factoid_def(self, key):
        key = key.lower()
        # first look through the factoids file
        # this line commented out because we like relative paths
        #with open(os.path.join(os.path.dirname(__file__), "resources", "factoids.txt")) as f:
        with open(os.path.join("resources", "factoids.txt")) as f:
            on_key = False
            found = False
            for l in f:
                on_key = not on_key

                if on_key:
                    if key.lower() in l[:-1].lower().split(" "):
                        found = True
                elif found:
                    return l[:-1]
        try:
            #with open(os.path.join(os.path.dirname(__file__), "resources", "randomfactoids", key+".qt")) as f:
            with open(os.path.join("resources", "randomfactoids", key+".qt")) as f:
                # use reservoir sampling algorithm to pick a random line from the qt file
                selection = None
                for i, l in enumerate(f):
                    if not random.randrange(i+1):
                        selection = l[:-1]
                return selection
        except FileNotFoundError:
            print("file not found")
        return None

    def ircget(self, msg):
        smsg = msg.split(" ")
        try:
            if smsg[1] == "PRIVMSG":
                stxt = smsg[3][1:].partition(self.prefix)
                if not stxt[0]:
                    fact = self.get_factoid_def(stxt[2])
                    if fact:
                        self.ircsend("PRIVMSG {} :{}".format(smsg[2], fact))

        except IndexError:
            pass

