import os
import random
import sqlite3

class Factoid:
    def __init__(self, ircsend, config):
        self.ircsend = ircsend
        self.dbfile = config['db']

        try:
            self.prefix = config['factoid prefix']
        except KeyError:
            self.prefix = '!'

    def get_factoid_def(self, key):
        with sqlite3.connect(self.dbfile) as conn:
            c = conn.execute('select def from names, definitions where name=? and names.factgroup=definitions.factgroup order by random() limit 1', (key,))
            result = c.fetchone()
            if result:
                return result[0]
            else:
                return None
    
    def ircget(self, msg):
        smsg = msg.split(" ")
        try:
            if smsg[1] == 'PRIVMSG':
                stxt = smsg[3][1:].partition(self.prefix)
                if not stxt[0]:
                    if stxt[2] == 'give':
                        output = smsg[4] + ': '
                        fact = self.get_factoid_def(smsg[5])
                    else:
                        output = ''
                        fact = self.get_factoid_def(stxt[2])
                    if fact:
                        if smsg[2].startswith('#'):
                            self.ircsend('PRIVMSG {} :{}'.format(smsg[2], output + fact))
                        else:
                            sender = smsg[0][1:].partition('!')[0]
                            self.ircsend('PRIVMSG {} :{}'.format(sender, output + fact))

        except IndexError:
            pass

