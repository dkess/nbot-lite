import random

class Choose:
    def __init__(self, ircsend, config):
        self.ircsend = ircsend

    def ircget(self, msg):
        smsg = msg.split(' ', 4)
        if len(smsg) == 5:
            sender = smsg[0][1:].partition('!')[0]
            if smsg[1] == 'PRIVMSG':
                if smsg[3] == ':.choose':
                    choice = random.choice(smsg[4].split(',')).strip()
                    if smsg[2].startswith('#') or smsg[2].startswith('&'):
                        self.ircsend('PRIVMSG {} :{}: {}'.format(smsg[2], sender, choice))
                    else:
                        self.ircsend('PRIVMSG {} :{}'.format(sender, choice))


