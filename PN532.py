import nfc
import time
import binascii


class PN532:
    def __init__(self, dev, aid, callback):
        self.dev = dev
        self.clf = None
        self.tagHandler = TagHandler(aid, callback)
        self.__setup()

    def __setup(self):
        self.clf = nfc.ContactlessFrontend(self.dev)

    def __connected(self, tag):
        self.tagHandler.handle(tag)
        return True

    def close(self):
        if (self.clf != None):
            self.clf.close()

    def listen(self):
        try:
            return self.clf.connect(rdwr={
                'on-connect': self.__connected,
                'on-discover': lambda target: True,
            })
        except Exception as e:
            print(e)
            # probably connection failed / timed out, reset connection
            self.close()
            self.__setup()
            return True


class TagHandler:
    def __init__(self, aid, callback):
        self.aid = aid
        self.callback = callback
        self.lastType2Tag = {'time': time.time(), 'uid': ''}

    def __byteArrayToHexString(self, bArray):
        return binascii.hexlify(bytearray(bArray)).decode('ascii').upper()

    def handle(self, tag):
        # detect type 2 tags: default chip / smartcard
        if hasattr(nfc.tag, 'tt2') and isinstance(tag, nfc.tag.tt2.Type2Tag):
            self.handleType2Tag(tag)
        # detect type4a tags: smartphone
        elif hasattr(nfc.tag, 'tt4') and isinstance(tag, nfc.tag.tt4.Type4ATag):
            self.handleType4ATag(tag)
        else:
            print("error: unsupported tag type")

    def handleType2Tag(self, tag):
        uid = self.__byteArrayToHexString(tag.identifier)
        # type2tag is_present attr is always False, so we need a bit of a cheat to detect it's release
        # if previous tag was detected > 1 second ago => this must be a new placed tag => callback
        if ((time.time() - self.lastType2Tag['time']) > 1.0) or uid != self.lastType2Tag['uid']:
            self.callback('Type2Tag', uid)

        # always reset time if tag is detected and save uid of tag
        # this happens at least once within a second, if the tag is placed on the reader
        # => callback above won't be called multiple times.
        self.lastType2Tag = {'time': time.time(), 'uid': uid}

    def handleType4ATag(self, tag):
        # AID, which will call service on android
        data = bytearray.fromhex(self.aid)

        cla = 0x00
        ins = 0xA4
        p1 = 0x04
        p2 = 0x00
        # CLA INS P1 P2, data => send apdu to android + get response
        data = tag.send_apdu(cla, ins, p1, p2, data, check_status=False)

        uid = self.__byteArrayToHexString(data)
        self.callback('Type4ATag', uid)
