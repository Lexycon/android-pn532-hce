import time
import sys
from PN532 import PN532

# allowedIDs = ['818F7C4B3CE1', '123456789']


def callbackPN532(tag, id):
    print('Found tag: {}, id: {}'.format(tag, id))
    # if (id in allowedIDs):
    #     print("ID valid :)")
    # else:
    #     print("ID invalid :(")


# device uart, aid for android, callback
pn532 = PN532('tty:AMA0', 'A0000001020304', callbackPN532)

while True:
    listen = pn532.listen()
    if not listen:
        break

pn532.close()
