#!/usr/bin/env python3

import socket

import channeljoin
import factoid

config = {'init':[]}
with open('config') as configfile:
    for l in configfile:
        key, _, val = l[:-1].partition("=")

        if key == 'init':
            config['init'].append(val)
        else:
            config[key] = val

print(config)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((config['server'], int(config['port'])))
except KeyError:
    print('You must specify a server and port in the config file.')

def ircsend(msg):
    global sock
    sock.send((msg + '\r\n').encode())
    print('<- ' + msg)

ircsend('USER %s 0 * :%s\r\nNICK %s\r\n' %
        (config['nick'],config['user'],config['nick']))

plugins = []
plugins.append(channeljoin.ChannelJoin(ircsend, config))
plugins.append(factoid.Factoid(ircsend, config))

while (1):
    data = sock.recv(512)
    try:
        decoded = data.decode()
    except UnicodeDecodeError:
        try:
            decoded = data.decode('latin1')
        except UnicodeDecodeError:
            continue
    for ircline in [l.rstrip('\r') for l in decoded.split('\n')][:-1]:
        print('-> '+ircline)
        if ircline.startswith('PING :'):
            ircsend('PONG :'+ircline[6:])
        else:
            for p in plugins:
                p.ircget(ircline)
