import nfc
import binascii


def byteArrayToHexString(bArray):
    return binascii.hexlify(bytearray(bArray)).decode('ascii')


def connected(tag):
    if hasattr(nfc.tag, 'tt2') and isinstance(tag, nfc.tag.tt2.Type2Tag):
        uid = byteArrayToHexString(tag.identifier)
        print('TAG2 (CARD), ID: {}'.format(uid))

    elif hasattr(nfc.tag, 'tt4') and isinstance(tag, nfc.tag.tt4.Type4ATag):
        cla = 0x00  # last or only command, no secure messaging, channel zero
        ins = 0xA4  # SELECT command
        p1 = 0x04   # Select by DF name
        p2 = 0x00   # First or only occurrence, Return FCI template
        aid = "A0000001020304"  # AID, which will call service on android
        data = bytearray.fromhex(aid)
        # send apdu + get response
        data = tag.send_apdu(cla, ins, p1, p2, data, check_status=False)
        uid = byteArrayToHexString(data)
        print('TAG4 (ANDROID), ID: {}'.format(uid))

    else:
        print("error: unknown tag type")

    return False


try:
    clf = nfc.ContactlessFrontend("tty:AMA0")
    tag = clf.connect(rdwr={'on-connect': connected,
                            'on-discover': lambda target: True})

finally:
    clf.close()
